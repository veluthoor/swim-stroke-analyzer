import logging
import os
import sys
import threading
import time
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# ---------------------------------------------------------------------------
# Path setup — allow imports from the project root
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from src.feedback_generator import FeedbackGenerator
from src.pose_detector import PoseDetector
from src.stroke_analyzer import StrokeAnalyzer
from src.video_processor import VideoProcessor
from src.visualizer import Visualizer

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App & CORS
# ---------------------------------------------------------------------------
app = Flask(__name__)

IS_PRODUCTION = os.getenv('FLASK_ENV', 'development') == 'production'
FRONTEND_URL = os.getenv('FRONTEND_URL', '')

if IS_PRODUCTION and FRONTEND_URL:
    allowed_origins = [FRONTEND_URL]
    logger.info(f"CORS: production mode, allowing origin: {FRONTEND_URL}")
else:
    # Development: allow both localhost variants
    allowed_origins = ['http://localhost:3000', 'http://127.0.0.1:3000']
    logger.info("CORS: development mode, allowing localhost:3000")

CORS(app, origins=allowed_origins)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(ROOT, 'backend', 'uploads')
RESULTS_FOLDER = os.path.join(ROOT, 'backend', 'results')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
MAX_FILE_SIZE = 200 * 1024 * 1024   # 200 MB — keeps memory & processing time sane
MAX_WORKERS = 3                      # Max concurrent video analyses
FILE_TTL_HOURS = 24                  # Auto-delete files older than this

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# ---------------------------------------------------------------------------
# Thread-safe job status store
# ---------------------------------------------------------------------------
processing_status: dict = {}
status_lock = threading.Lock()


def _set_status(video_id: str, **kwargs):
    with status_lock:
        if video_id in processing_status:
            processing_status[video_id].update(kwargs)


def _get_status(video_id: str) -> dict:
    with status_lock:
        return dict(processing_status.get(video_id, {}))


# ---------------------------------------------------------------------------
# Thread pool — limits concurrent analyses to MAX_WORKERS
# ---------------------------------------------------------------------------
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# ---------------------------------------------------------------------------
# Simple in-memory rate limiter (per IP, sliding window)
# ---------------------------------------------------------------------------
_request_log: dict = defaultdict(list)
_rate_lock = threading.Lock()
RATE_LIMIT_REQUESTS = 10   # max uploads per IP
RATE_LIMIT_WINDOW = 3600   # …within this many seconds (1 hour)


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        # Purge expired entries
        _request_log[ip] = [t for t in _request_log[ip] if now - t < RATE_LIMIT_WINDOW]
        if len(_request_log[ip]) >= RATE_LIMIT_REQUESTS:
            return True
        _request_log[ip].append(now)
        return False


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------
def _allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _validate_video_magic(file_path: str) -> bool:
    """
    Check magic bytes to confirm the file is actually a video container,
    not an executable disguised with a .mp4 extension.
    """
    try:
        with open(file_path, 'rb') as fh:
            header = fh.read(12)
        # MP4 / MOV: bytes 4–7 are an ISOM box type
        if header[4:8] in (b'ftyp', b'moov', b'mdat', b'wide', b'free'):
            return True
        # AVI: RIFF....AVI
        if header[:4] == b'RIFF' and header[8:12] == b'AVI ':
            return True
        return False
    except Exception:
        return False


def _cleanup_old_files():
    """Delete upload/result files older than FILE_TTL_HOURS."""
    cutoff = time.time() - FILE_TTL_HOURS * 3600
    for folder in (UPLOAD_FOLDER, RESULTS_FOLDER):
        try:
            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                try:
                    if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                        os.remove(path)
                        logger.info(f"Cleaned up expired file: {path}")
                except OSError as exc:
                    logger.warning(f"Could not remove {path}: {exc}")
        except OSError as exc:
            logger.warning(f"Could not list {folder}: {exc}")


# Run cleanup once at startup
_cleanup_old_files()


# ---------------------------------------------------------------------------
# Video processing (runs in thread pool worker)
# ---------------------------------------------------------------------------
def _process_video(video_id: str, input_path: str, output_path: str, report_path: str):
    """Full analysis pipeline executed in a pool worker thread."""
    try:
        _set_status(video_id, status='processing', progress=10,
                    message='Detecting poses...')

        pose_detector = PoseDetector()
        stroke_analyzer = StrokeAnalyzer()
        visualizer = Visualizer()
        feedback_generator = FeedbackGenerator()

        poses = pose_detector.process_video(input_path)
        _set_status(video_id, progress=50, message='Analyzing stroke mechanics...')

        analysis = stroke_analyzer.analyze_video(poses)
        _set_status(video_id, progress=65, message='Generating annotated video...')

        visualizer.create_annotated_video(poses, output_path, analysis, input_path)
        _set_status(video_id, progress=85, message='Re-encoding for browser...')

        # Best-effort ffmpeg re-encode; non-fatal if ffmpeg is absent
        reencoded = VideoProcessor.reencode_for_browser(output_path)
        if not reencoded:
            logger.warning(f"[{video_id}] ffmpeg re-encode skipped — video may not play in all browsers")

        _set_status(video_id, progress=92, message='Generating report...')

        report = feedback_generator.generate_report(analysis)
        with open(report_path, 'w') as fh:
            fh.write(report)

        _set_status(video_id, status='completed', progress=100,
                    message='Analysis complete!')
        logger.info(f"[{video_id}] Analysis completed successfully")

    except Exception as exc:
        import traceback
        logger.error(f"[{video_id}] Analysis failed:\n{traceback.format_exc()}")
        _set_status(video_id, status='failed', error=str(exc))
    finally:
        # Clean up the raw upload to save disk space
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Accept a video upload and queue it for analysis."""
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if _is_rate_limited(client_ip):
        logger.warning(f"Rate limit exceeded for {client_ip}")
        return jsonify({'error': 'Too many uploads. Please try again later.'}), 429

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400

    if not _allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: MP4, AVI, MOV'}), 400

    video_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()

    input_path = os.path.join(UPLOAD_FOLDER, f'{video_id}.{ext}')
    output_path = os.path.join(RESULTS_FOLDER, f'{video_id}_analyzed.mp4')
    report_path = os.path.join(RESULTS_FOLDER, f'{video_id}_report.txt')

    file.save(input_path)

    # Validate it's actually a video (magic bytes check)
    if not _validate_video_magic(input_path):
        os.remove(input_path)
        return jsonify({'error': 'File does not appear to be a valid video'}), 400

    with status_lock:
        processing_status[video_id] = {
            'status': 'queued',
            'progress': 0,
            'message': 'Upload complete, queued for analysis...',
        }

    executor.submit(_process_video, video_id, input_path, output_path, report_path)
    logger.info(f"[{video_id}] Queued for analysis (from {client_ip})")

    return jsonify({'video_id': video_id, 'message': 'Upload successful, analysis queued'}), 200


@app.route('/api/status/<video_id>', methods=['GET'])
def get_status(video_id):
    status = _get_status(video_id)
    if not status:
        return jsonify({'error': 'Video not found'}), 404
    return jsonify(status), 200


@app.route('/api/result/<video_id>/video', methods=['GET'])
def get_result_video(video_id):
    # Results are always saved as .mp4
    video_path = os.path.join(RESULTS_FOLDER, f'{video_id}_analyzed.mp4')
    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4', as_attachment=False)

    # Fallback: check other extensions (e.g. AVI if re-encode was skipped)
    for ext in ALLOWED_EXTENSIONS:
        alt_path = os.path.join(RESULTS_FOLDER, f'{video_id}_analyzed.{ext}')
        if os.path.exists(alt_path):
            mimetype = 'video/mp4' if ext == 'mp4' else f'video/{ext}'
            return send_file(alt_path, mimetype=mimetype, as_attachment=False)

    return jsonify({'error': 'Video result not found'}), 404


@app.route('/api/result/<video_id>/report', methods=['GET'])
def get_result_report(video_id):
    report_path = os.path.join(RESULTS_FOLDER, f'{video_id}_report.txt')
    if not os.path.exists(report_path):
        return jsonify({'error': 'Report not found'}), 404
    with open(report_path, 'r') as fh:
        return jsonify({'report': fh.read()}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'workers': MAX_WORKERS}), 200


# ---------------------------------------------------------------------------
# Entry point (dev server only — production uses gunicorn)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=not IS_PRODUCTION, host='0.0.0.0', port=5001)
