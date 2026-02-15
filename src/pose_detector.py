"""Pose detection using MediaPipe for swimming stroke analysis."""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Optional


class PoseDetector:
    """Detects and tracks swimmer pose using MediaPipe."""

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize MediaPipe Pose detector."""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1  # Balanced speed/accuracy (was 2, way too slow)
        )

        # Key landmarks for swimming analysis
        self.LANDMARKS = {
            'nose': 0,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28,
        }

    def detect_pose(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Detect pose in a single frame.

        Args:
            frame: BGR image from OpenCV

        Returns:
            Dictionary containing landmarks and metadata, or None if no pose detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame
        results = self.pose.process(rgb_frame)

        if not results.pose_landmarks:
            return None

        # Extract landmark coordinates
        h, w, _ = frame.shape
        landmarks = {}

        for name, idx in self.LANDMARKS.items():
            landmark = results.pose_landmarks.landmark[idx]
            landmarks[name] = {
                'x': landmark.x * w,
                'y': landmark.y * h,
                'z': landmark.z,  # Relative depth
                'visibility': landmark.visibility
            }

        return {
            'landmarks': landmarks,
            'raw_landmarks': results.pose_landmarks,
            'frame_shape': (h, w)
        }

    def process_video(self, video_path: str, skip_frames: int = 2) -> List[Dict]:
        """
        Process video and extract pose data (skips frames for speed).

        Args:
            video_path: Path to video file
            skip_frames: Process every Nth frame (2 = 2x faster, 3 = 3x faster)

        Returns:
            List of pose data dictionaries, one per processed frame
        """
        cap = cv2.VideoCapture(video_path)
        pose_data = []

        frame_count = 0
        processed_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        print(f"Processing video: {total_frames} frames at {fps:.2f} fps (analyzing every {skip_frames} frames)")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames for performance
            if frame_count % skip_frames != 0:
                frame_count += 1
                continue

            pose_result = self.detect_pose(frame)
            processed_count += 1

            pose_data.append({
                'frame_number': frame_count,
                'timestamp': frame_count / fps,
                'pose': pose_result,
                # NOTE: frames are NOT stored here to avoid memory exhaustion.
                # The visualizer re-reads frames directly from the source video.
            })

            frame_count += 1
            if processed_count % 15 == 0:  # Show progress more often
                pct = (frame_count / total_frames) * 100
                print(f"Progress: {pct:.1f}% ({processed_count} frames analyzed)")

        cap.release()
        print(f"✓ Completed: {processed_count} frames analyzed ({total_frames} total, skipped {total_frames - processed_count})")

        return pose_data

    def calculate_angle(self, point1: Dict, point2: Dict, point3: Dict) -> float:
        """
        Calculate angle between three points.

        Args:
            point1, point2, point3: Landmark dictionaries with 'x' and 'y' keys
            point2 is the vertex of the angle

        Returns:
            Angle in degrees
        """
        # Convert to numpy arrays
        p1 = np.array([point1['x'], point1['y']])
        p2 = np.array([point2['x'], point2['y']])
        p3 = np.array([point3['x'], point3['y']])

        # Calculate vectors
        v1 = p1 - p2
        v2 = p3 - p2

        # Calculate angle
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Handle numerical errors
        angle = np.arccos(cos_angle)

        return np.degrees(angle)

    def calculate_body_rotation(self, landmarks: Dict) -> float:
        """
        Calculate body rotation angle from shoulder-hip line.

        Args:
            landmarks: Dictionary of landmark positions

        Returns:
            Rotation angle in degrees (0 = flat, 90 = on side)
        """
        # Use shoulder width vs hip width to estimate rotation
        shoulder_width = abs(landmarks['left_shoulder']['x'] - landmarks['right_shoulder']['x'])
        hip_width = abs(landmarks['left_hip']['x'] - landmarks['right_hip']['x'])

        # In perfect side view, one shoulder/hip would be hidden
        # Wider = more frontal view
        # This is a simplified approximation
        avg_width = (shoulder_width + hip_width) / 2

        # Normalize and convert to rotation estimate
        # This is rough - proper rotation needs 3D analysis or multiple cameras
        rotation = 90 - (avg_width / 100 * 90)  # Simplified heuristic

        return max(0, min(90, rotation))

    def __del__(self):
        """Cleanup MediaPipe resources."""
        if hasattr(self, 'pose'):
            self.pose.close()
