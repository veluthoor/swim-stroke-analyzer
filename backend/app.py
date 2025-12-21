from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename
import uuid
import threading

# Add parent directory to path to import analyzer modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pose_detector import PoseDetector
from src.stroke_analyzer import StrokeAnalyzer
from src.visualizer import Visualizer
from src.feedback_generator import FeedbackGenerator

app = Flask(__name__)

# Enable CORS for React frontend
# Allow all origins in development, specific origin in production
allowed_origins = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, origins=[allowed_origins, 'http://localhost:3000'])

# Configuration
UPLOAD_FOLDER = 'backend/uploads'
RESULTS_FOLDER = 'backend/results'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Store processing status
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video(video_id, input_path, output_path, report_path):
    """Process video in background thread"""
    try:
        processing_status[video_id]['status'] = 'processing'
        processing_status[video_id]['progress'] = 10

        # Initialize components
        pose_detector = PoseDetector()
        stroke_analyzer = StrokeAnalyzer()
        visualizer = Visualizer()
        feedback_generator = FeedbackGenerator()

        processing_status[video_id]['progress'] = 20
        processing_status[video_id]['message'] = 'Analyzing video...'

        # Detect poses
        poses = pose_detector.process_video(input_path)
        processing_status[video_id]['progress'] = 50

        # Analyze stroke
        analysis = stroke_analyzer.analyze_video(poses)
        processing_status[video_id]['progress'] = 70
        processing_status[video_id]['message'] = 'Generating annotated video...'

        # Create annotated video
        visualizer.create_annotated_video(poses, output_path, analysis, input_path)
        processing_status[video_id]['progress'] = 90

        # Generate report
        report = feedback_generator.generate_report(analysis)
        with open(report_path, 'w') as f:
            f.write(report)

        processing_status[video_id]['status'] = 'completed'
        processing_status[video_id]['progress'] = 100
        processing_status[video_id]['message'] = 'Analysis complete!'

    except Exception as e:
        import traceback
        processing_status[video_id]['status'] = 'failed'
        processing_status[video_id]['error'] = str(e)
        print(f"\n{'='*60}")
        print(f"ERROR processing video {video_id}:")
        print(f"{'='*60}")
        print(traceback.format_exc())
        print(f"{'='*60}\n")

@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Handle video upload"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: MP4, AVI, MOV'}), 400

    # Generate unique ID for this upload
    video_id = str(uuid.uuid4())

    # Save uploaded file
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{video_id}.{ext}')
    output_path = os.path.join(app.config['RESULTS_FOLDER'], f'{video_id}_analyzed.{ext}')
    report_path = os.path.join(app.config['RESULTS_FOLDER'], f'{video_id}_report.txt')

    file.save(input_path)

    # Initialize processing status
    processing_status[video_id] = {
        'status': 'queued',
        'progress': 0,
        'message': 'Upload complete, starting analysis...'
    }

    # Start processing in background thread
    thread = threading.Thread(
        target=process_video,
        args=(video_id, input_path, output_path, report_path)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        'video_id': video_id,
        'message': 'Video uploaded successfully, processing started'
    }), 200

@app.route('/api/status/<video_id>', methods=['GET'])
def get_status(video_id):
    """Get processing status for a video"""
    if video_id not in processing_status:
        return jsonify({'error': 'Video not found'}), 404

    return jsonify(processing_status[video_id]), 200

@app.route('/api/result/<video_id>/video', methods=['GET'])
def get_result_video(video_id):
    """Stream analyzed video for playback"""
    # Find the file with any extension
    for ext in ALLOWED_EXTENSIONS:
        video_path = os.path.join(app.config['RESULTS_FOLDER'], f'{video_id}_analyzed.{ext}')
        if os.path.exists(video_path):
            # Determine correct mimetype
            mimetype = 'video/mp4' if ext == 'mp4' else f'video/{ext}'
            # Use as_attachment=False to allow inline playback
            return send_file(
                video_path,
                mimetype=mimetype,
                as_attachment=False,
                download_name=f'{video_id}_analyzed.{ext}'
            )

    return jsonify({'error': 'Video not found'}), 404

@app.route('/api/result/<video_id>/report', methods=['GET'])
def get_result_report(video_id):
    """Get text report"""
    report_path = os.path.join(app.config['RESULTS_FOLDER'], f'{video_id}_report.txt')

    if not os.path.exists(report_path):
        return jsonify({'error': 'Report not found'}), 404

    with open(report_path, 'r') as f:
        report = f.read()

    return jsonify({'report': report}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
