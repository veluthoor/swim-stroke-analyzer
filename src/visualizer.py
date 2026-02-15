"""Visualizes pose data and annotations on video."""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Optional
from src.video_processor import VideoProcessor
from src.models.freestyle_rules import get_severity_emoji


class Visualizer:
    """Creates annotated videos with pose overlays and metrics."""

    def __init__(self):
        """Initialize visualizer."""
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=2)

        # Colors (BGR format)
        self.COLOR_SKELETON = (0, 255, 0)  # Green
        self.COLOR_CRITICAL = (0, 0, 255)  # Red
        self.COLOR_MODERATE = (0, 165, 255)  # Orange
        self.COLOR_MINOR = (255, 255, 0)  # Cyan
        self.COLOR_TEXT_BG = (0, 0, 0)  # Black
        self.COLOR_TEXT = (255, 255, 255)  # White

    def create_annotated_video(
        self,
        pose_data: List[Dict],
        output_path: str,
        analysis_results: Dict,
        original_video_path: str
    ) -> str:
        """
        Create annotated video with pose overlay and metrics.

        Frames are re-read directly from the original video (pose_data no longer
        stores frames) to avoid memory exhaustion on long videos.

        Args:
            pose_data: List of frame data with pose information (no 'frame' key)
            output_path: Path to save annotated video
            analysis_results: Results from stroke analyzer
            original_video_path: Path to original video for metadata

        Returns:
            Path to created video
        """
        if not pose_data:
            raise ValueError("No pose data to visualize")

        # Build a fast lookup: frame_number -> pose
        pose_lookup = {fd['frame_number']: fd['pose'] for fd in pose_data}

        # Get video properties
        video_info = VideoProcessor(original_video_path).get_video_info()
        total_frames = video_info['frame_count']

        # Create video writer
        writer = VideoProcessor.create_video_writer(
            output_path,
            video_info['fps'],
            video_info['width'],
            video_info['height']
        )

        # Re-open original video for frame-by-frame reading
        cap = cv2.VideoCapture(original_video_path)

        print(f"\nCreating annotated video...")
        print(f"Output: {output_path}")

        frame_idx = 0
        last_pose = None  # Forward-fill pose on frames that were skipped during analysis

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Use analyzed pose for this frame, or forward-fill from last known pose
            if frame_idx in pose_lookup:
                last_pose = pose_lookup[frame_idx]
            pose = last_pose

            # Draw pose if detected
            if pose is not None:
                frame = self._draw_pose(frame, pose)
                frame = self._draw_metrics_overlay(frame, pose, analysis_results)

            # Draw overall stats in corner
            frame = self._draw_stats_panel(frame, analysis_results, frame_idx, total_frames)

            writer.write(frame)
            frame_idx += 1

            if frame_idx % 30 == 0:
                print(f"Rendered {frame_idx}/{total_frames} frames")

        cap.release()
        writer.release()
        print(f"Completed: {output_path}")

        return output_path

    def _draw_pose(self, frame: np.ndarray, pose: Dict) -> np.ndarray:
        """Draw pose skeleton on frame."""
        if pose['raw_landmarks'] is None:
            return frame

        # Draw landmarks and connections
        self.mp_drawing.draw_landmarks(
            frame,
            pose['raw_landmarks'],
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                color=self.COLOR_SKELETON,
                thickness=2,
                circle_radius=3
            ),
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=self.COLOR_SKELETON,
                thickness=2
            )
        )

        return frame

    def _draw_metrics_overlay(self, frame: np.ndarray, pose: Dict, analysis: Dict) -> np.ndarray:
        """Draw real-time metrics overlay on frame."""
        landmarks = pose['landmarks']

        # Draw elbow angle
        if analysis['metrics'].get('elbow', {}).get('avg_angle') is not None:
            # Left elbow
            left_shoulder = landmarks['left_shoulder']
            left_elbow = landmarks['left_elbow']
            left_wrist = landmarks['left_wrist']

            if (left_shoulder['visibility'] > 0.5 and
                left_elbow['visibility'] > 0.5 and
                left_wrist['visibility'] > 0.5):

                angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
                elbow_pos = (int(left_elbow['x']), int(left_elbow['y']))

                # Color based on angle quality
                color = self._get_angle_color(angle, 80, 100, 120)
                self._draw_angle_annotation(frame, elbow_pos, angle, color)

        return frame

    def _draw_stats_panel(
        self,
        frame: np.ndarray,
        analysis: Dict,
        current_frame: int,
        total_frames: int
    ) -> np.ndarray:
        """Draw stats panel in corner of frame."""
        h, w = frame.shape[:2]

        # Semi-transparent overlay
        overlay = frame.copy()
        panel_height = 200
        cv2.rectangle(overlay, (0, 0), (400, panel_height), self.COLOR_TEXT_BG, -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        # Draw text
        y_offset = 30
        line_height = 25

        # Title
        self._draw_text(frame, "FREESTYLE ANALYSIS", (10, y_offset), scale=0.6, thickness=2)
        y_offset += line_height + 5

        # Metrics
        metrics = analysis['metrics']

        if metrics.get('elbow', {}).get('avg_angle') is not None:
            elbow_avg = metrics['elbow']['avg_angle']
            color = self._get_angle_color(elbow_avg, 80, 100, 120)
            self._draw_text(
                frame,
                f"Elbow Angle: {elbow_avg:.0f}deg",
                (10, y_offset),
                scale=0.5,
                color=color
            )
            y_offset += line_height

        if metrics.get('rotation', {}).get('avg_rotation') is not None:
            rotation_avg = metrics['rotation']['avg_rotation']
            color = self._get_angle_color(rotation_avg, 45, 60, 30, reverse=True)
            self._draw_text(
                frame,
                f"Body Rotation: {rotation_avg:.0f}deg",
                (10, y_offset),
                scale=0.5,
                color=color
            )
            y_offset += line_height

        if metrics.get('stroke_rate', {}).get('spm') is not None:
            spm = metrics['stroke_rate']['spm']
            self._draw_text(
                frame,
                f"Stroke Rate: {spm:.0f} SPM",
                (10, y_offset),
                scale=0.5
            )
            y_offset += line_height

        # Progress bar
        progress = current_frame / total_frames
        bar_width = 380
        bar_height = 10
        bar_x = 10
        bar_y = panel_height - 30

        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)

        return frame

    def _draw_angle_annotation(
        self,
        frame: np.ndarray,
        position: tuple,
        angle: float,
        color: tuple
    ):
        """Draw angle annotation at position."""
        text = f"{angle:.0f}deg"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        thickness = 2

        # Get text size for background
        (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)

        # Draw background
        bg_x1 = position[0] - 5
        bg_y1 = position[1] - text_h - 10
        bg_x2 = position[0] + text_w + 5
        bg_y2 = position[1] - 5

        cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), self.COLOR_TEXT_BG, -1)

        # Draw text
        cv2.putText(frame, text, (position[0], position[1] - 10), font, scale, color, thickness)

    def _draw_text(
        self,
        frame: np.ndarray,
        text: str,
        position: tuple,
        scale: float = 0.5,
        color: tuple = None,
        thickness: int = 1
    ):
        """Draw text with optional background."""
        if color is None:
            color = self.COLOR_TEXT

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, position, font, scale, color, thickness, cv2.LINE_AA)

    def _get_angle_color(
        self,
        angle: float,
        optimal_min: float,
        optimal_max: float,
        critical_threshold: float,
        reverse: bool = False
    ) -> tuple:
        """Get color based on angle quality."""
        if reverse:
            # For metrics where lower is worse
            if angle < critical_threshold:
                return self.COLOR_CRITICAL
            elif angle < optimal_min:
                return self.COLOR_MODERATE
            else:
                return self.COLOR_SKELETON
        else:
            # For metrics where higher is worse
            if optimal_min <= angle <= optimal_max:
                return self.COLOR_SKELETON
            elif angle > critical_threshold:
                return self.COLOR_CRITICAL
            else:
                return self.COLOR_MODERATE

    @staticmethod
    def _calculate_angle(point1: Dict, point2: Dict, point3: Dict) -> float:
        """Calculate angle between three points."""
        p1 = np.array([point1['x'], point1['y']])
        p2 = np.array([point2['x'], point2['y']])
        p3 = np.array([point3['x'], point3['y']])

        v1 = p1 - p2
        v2 = p3 - p2

        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)

        return np.degrees(angle)
