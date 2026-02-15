"""Video input/output processing utilities."""

import cv2
import os
import subprocess
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handles video file operations."""

    def __init__(self, video_path: str):
        """Initialize video processor."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video file: {video_path}")

        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.frame_count / self.fps if self.fps > 0 else 0

        self.cap.release()  # Close until needed

    def get_video_info(self) -> dict:
        """Get video metadata."""
        return {
            'path': self.video_path,
            'fps': self.fps,
            'frame_count': self.frame_count,
            'width': self.width,
            'height': self.height,
            'duration': self.duration
        }

    @staticmethod
    def create_video_writer(output_path: str, fps: float, width: int, height: int) -> cv2.VideoWriter:
        """
        Create video writer for output.

        Args:
            output_path: Path to save output video
            fps: Frames per second
            width: Frame width
            height: Frame height

        Returns:
            OpenCV VideoWriter object
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        # Try H.264 first — works natively on macOS and when libx264 is installed.
        # On Linux servers H.264 often requires ffmpeg; we fall back to mp4v and
        # re-encode afterwards via VideoProcessor.reencode_for_browser().
        for fourcc_str in ('avc1', 'H264', 'X264'):
            fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if writer.isOpened():
                logger.debug(f"VideoWriter opened with codec '{fourcc_str}'")
                return writer
            writer.release()

        # Universal fallback — supported everywhere by OpenCV.
        # Call reencode_for_browser() after writing to make it playable in browsers.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if writer.isOpened():
            logger.warning(
                "VideoWriter fell back to mp4v codec. "
                "Call reencode_for_browser() after writing for browser compatibility."
            )
            return writer

        raise ValueError(f"Failed to create video writer for: {output_path}")

    @staticmethod
    def generate_output_path(input_path: str, suffix: str = "_analyzed") -> str:
        """
        Generate output path based on input path.

        Args:
            input_path: Input video path
            suffix: Suffix to add to filename

        Returns:
            Output path string
        """
        base, ext = os.path.splitext(input_path)
        return f"{base}{suffix}{ext}"

    @staticmethod
    def reencode_for_browser(video_path: str) -> bool:
        """
        Re-encode a video to H.264 MP4 using ffmpeg so it plays in browsers.

        Performs an in-place replacement: writes to a temp file then atomically
        renames it over the original.  Safe to call even if ffmpeg is absent —
        returns False in that case so the caller can decide how to handle it.

        Args:
            video_path: Path to the video file to re-encode in-place.

        Returns:
            True on success, False if ffmpeg is unavailable or encoding failed.
        """
        base, ext = os.path.splitext(video_path)
        temp_path = f"{base}_reenc{ext}"

        try:
            # Verify ffmpeg is available
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True, check=True, timeout=10
            )

            result = subprocess.run(
                [
                    'ffmpeg', '-y',
                    '-i', video_path,
                    '-vcodec', 'libx264',
                    '-preset', 'fast',
                    '-crf', '23',
                    '-acodec', 'aac',
                    '-movflags', '+faststart',  # Progressive download / streaming
                    temp_path
                ],
                capture_output=True,
                timeout=900  # 15-minute ceiling for very long videos
            )

            if result.returncode == 0 and os.path.exists(temp_path):
                os.replace(temp_path, video_path)
                logger.info(f"Re-encoded for browser: {video_path}")
                return True

            logger.warning(
                f"ffmpeg re-encode failed (exit {result.returncode}): "
                f"{result.stderr.decode(errors='replace')[:500]}"
            )
            return False

        except FileNotFoundError:
            logger.warning("ffmpeg not found — skipping browser re-encode")
            return False
        except subprocess.TimeoutExpired:
            logger.warning("ffmpeg re-encode timed out")
            return False
        except Exception as exc:
            logger.warning(f"ffmpeg re-encode error: {exc}")
            return False
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
