"""Video input/output processing utilities."""

import cv2
import os
from typing import Tuple, Optional


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

        # Use mp4v codec for MP4 files
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        if not writer.isOpened():
            raise ValueError(f"Failed to create video writer: {output_path}")

        return writer

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
