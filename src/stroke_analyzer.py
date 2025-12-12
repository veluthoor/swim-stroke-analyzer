"""Analyzes swimming stroke metrics and detects technique issues."""

import numpy as np
from typing import List, Dict, Tuple, Optional
from src.models.freestyle_rules import (
    ELBOW_ANGLE_OPTIMAL_MIN, ELBOW_ANGLE_OPTIMAL_MAX, ELBOW_ANGLE_DROPPED,
    BODY_ROTATION_OPTIMAL_MIN, BODY_ROTATION_OPTIMAL_MAX,
    BODY_ROTATION_TOO_FLAT, BODY_ROTATION_TOO_MUCH,
    ARM_ENTRY_CENTERLINE_THRESHOLD, HEAD_LIFT_THRESHOLD,
    STROKE_RATE_OPTIMAL_MIN, STROKE_RATE_OPTIMAL_MAX,
    KNEE_ANGLE_OPTIMAL, KNEE_ANGLE_EXCESSIVE_BEND,
    MIN_VISIBILITY, FreestyleIssue, ISSUE_TYPES,
    SEVERITY_CRITICAL, SEVERITY_MODERATE, SEVERITY_MINOR
)


class StrokeAnalyzer:
    """Analyzes freestyle swimming technique from pose data."""

    def __init__(self):
        """Initialize stroke analyzer."""
        self.metrics = {}
        self.issues = []

    def analyze_video(self, pose_data: List[Dict]) -> Dict:
        """
        Analyze complete video pose data.

        Args:
            pose_data: List of frame data with pose information

        Returns:
            Dictionary containing metrics and detected issues
        """
        print("\nAnalyzing stroke mechanics...")

        # Filter frames with valid pose data
        valid_frames = [frame for frame in pose_data if frame['pose'] is not None]

        if len(valid_frames) == 0:
            return {
                'error': 'No valid pose data detected in video',
                'metrics': {},
                'issues': []
            }

        print(f"Valid frames: {len(valid_frames)}/{len(pose_data)}")

        # Analyze different aspects
        elbow_metrics = self._analyze_elbow_angles(valid_frames)
        rotation_metrics = self._analyze_body_rotation(valid_frames)
        entry_metrics = self._analyze_arm_entry(valid_frames)
        head_metrics = self._analyze_head_position(valid_frames)
        stroke_rate_metrics = self._analyze_stroke_rate(valid_frames)
        kick_metrics = self._analyze_kick(valid_frames)

        # Combine all metrics
        self.metrics = {
            'elbow': elbow_metrics,
            'rotation': rotation_metrics,
            'entry': entry_metrics,
            'head': head_metrics,
            'stroke_rate': stroke_rate_metrics,
            'kick': kick_metrics,
            'valid_frame_ratio': len(valid_frames) / len(pose_data)
        }

        # Detect issues based on metrics
        self.issues = self._detect_issues()

        return {
            'metrics': self.metrics,
            'issues': self.issues
        }

    def _analyze_elbow_angles(self, frames: List[Dict]) -> Dict:
        """Analyze elbow angles during catch phase."""
        left_elbow_angles = []
        right_elbow_angles = []

        for frame in frames:
            landmarks = frame['pose']['landmarks']

            # Check visibility
            if (landmarks['left_shoulder']['visibility'] < MIN_VISIBILITY or
                landmarks['left_elbow']['visibility'] < MIN_VISIBILITY or
                landmarks['left_wrist']['visibility'] < MIN_VISIBILITY):
                continue

            # Calculate left elbow angle
            angle = self._calculate_angle(
                landmarks['left_shoulder'],
                landmarks['left_elbow'],
                landmarks['left_wrist']
            )
            left_elbow_angles.append(angle)

            # Calculate right elbow angle
            if (landmarks['right_shoulder']['visibility'] >= MIN_VISIBILITY and
                landmarks['right_elbow']['visibility'] >= MIN_VISIBILITY and
                landmarks['right_wrist']['visibility'] >= MIN_VISIBILITY):

                angle = self._calculate_angle(
                    landmarks['right_shoulder'],
                    landmarks['right_elbow'],
                    landmarks['right_wrist']
                )
                right_elbow_angles.append(angle)

        all_angles = left_elbow_angles + right_elbow_angles

        return {
            'avg_angle': np.mean(all_angles) if all_angles else None,
            'min_angle': np.min(all_angles) if all_angles else None,
            'max_angle': np.max(all_angles) if all_angles else None,
            'left_avg': np.mean(left_elbow_angles) if left_elbow_angles else None,
            'right_avg': np.mean(right_elbow_angles) if right_elbow_angles else None,
        }

    def _analyze_body_rotation(self, frames: List[Dict]) -> Dict:
        """Analyze body rotation throughout stroke cycle."""
        rotations = []

        for frame in frames:
            landmarks = frame['pose']['landmarks']

            # Simplified rotation calculation using shoulder and hip width
            shoulder_width = abs(landmarks['left_shoulder']['x'] - landmarks['right_shoulder']['x'])
            hip_width = abs(landmarks['left_hip']['x'] - landmarks['right_hip']['x'])

            # Average the two
            avg_width = (shoulder_width + hip_width) / 2
            frame_width = frame['pose']['frame_shape'][1]

            # Normalize and estimate rotation
            # This is approximate - proper rotation needs 3D or multiple angles
            width_ratio = avg_width / frame_width
            estimated_rotation = 90 - (width_ratio * 180)  # Heuristic

            # Clamp to reasonable range
            estimated_rotation = max(0, min(90, estimated_rotation))
            rotations.append(estimated_rotation)

        return {
            'avg_rotation': np.mean(rotations) if rotations else None,
            'min_rotation': np.min(rotations) if rotations else None,
            'max_rotation': np.max(rotations) if rotations else None,
            'std_rotation': np.std(rotations) if rotations else None,
        }

    def _analyze_arm_entry(self, frames: List[Dict]) -> Dict:
        """Analyze arm entry position relative to centerline."""
        centerline_crossings = []

        for frame in frames:
            landmarks = frame['pose']['landmarks']
            frame_width = frame['pose']['frame_shape'][1]

            # Calculate body centerline (midpoint between shoulders)
            center_x = (landmarks['left_shoulder']['x'] + landmarks['right_shoulder']['x']) / 2

            # Check left wrist entry
            if landmarks['left_wrist']['visibility'] >= MIN_VISIBILITY:
                left_distance = abs(landmarks['left_wrist']['x'] - center_x)
                left_crossing = left_distance / frame_width
                centerline_crossings.append(left_crossing)

            # Check right wrist entry
            if landmarks['right_wrist']['visibility'] >= MIN_VISIBILITY:
                right_distance = abs(landmarks['right_wrist']['x'] - center_x)
                right_crossing = right_distance / frame_width
                centerline_crossings.append(right_crossing)

        return {
            'avg_centerline_distance': np.mean(centerline_crossings) if centerline_crossings else None,
            'max_crossing': np.max(centerline_crossings) if centerline_crossings else None,
        }

    def _analyze_head_position(self, frames: List[Dict]) -> Dict:
        """Analyze head stability and lifting during breathing."""
        nose_y_positions = []

        for frame in frames:
            landmarks = frame['pose']['landmarks']
            if landmarks['nose']['visibility'] >= MIN_VISIBILITY:
                nose_y_positions.append(landmarks['nose']['y'])

        if not nose_y_positions:
            return {'stability': None}

        # Calculate vertical movement range
        y_range = np.max(nose_y_positions) - np.min(nose_y_positions)
        frame_height = frames[0]['pose']['frame_shape'][0]
        normalized_range = y_range / frame_height

        return {
            'vertical_movement': normalized_range,
            'avg_y': np.mean(nose_y_positions),
            'stability': 1.0 - normalized_range  # Higher = more stable
        }

    def _analyze_stroke_rate(self, frames: List[Dict]) -> Dict:
        """Analyze stroke rate (strokes per minute)."""
        # Detect stroke cycles by tracking wrist position peaks
        # This is simplified - proper stroke detection needs more sophisticated algorithm

        if len(frames) < 2:
            return {'spm': None}

        # Get video duration
        duration = frames[-1]['timestamp'] - frames[0]['timestamp']

        # Count approximate strokes by detecting wrist forward movement peaks
        # Very simplified for MVP
        left_wrist_x = []
        for frame in frames:
            landmarks = frame['pose']['landmarks']
            if landmarks['left_wrist']['visibility'] >= MIN_VISIBILITY:
                left_wrist_x.append(landmarks['left_wrist']['x'])

        # Count peaks (forward reaches)
        if len(left_wrist_x) < 10:
            return {'spm': None}

        peaks = 0
        for i in range(1, len(left_wrist_x) - 1):
            if left_wrist_x[i] > left_wrist_x[i-1] and left_wrist_x[i] > left_wrist_x[i+1]:
                peaks += 1

        # Calculate strokes per minute (2 arms)
        strokes = peaks * 2
        spm = (strokes / duration) * 60 if duration > 0 else None

        return {
            'spm': spm,
            'total_strokes': strokes,
            'duration': duration
        }

    def _analyze_kick(self, frames: List[Dict]) -> Dict:
        """Analyze kick technique - knee bend."""
        knee_angles = []

        for frame in frames:
            landmarks = frame['pose']['landmarks']

            # Left leg
            if (landmarks['left_hip']['visibility'] >= MIN_VISIBILITY and
                landmarks['left_knee']['visibility'] >= MIN_VISIBILITY and
                landmarks['left_ankle']['visibility'] >= MIN_VISIBILITY):

                angle = self._calculate_angle(
                    landmarks['left_hip'],
                    landmarks['left_knee'],
                    landmarks['left_ankle']
                )
                knee_angles.append(angle)

            # Right leg
            if (landmarks['right_hip']['visibility'] >= MIN_VISIBILITY and
                landmarks['right_knee']['visibility'] >= MIN_VISIBILITY and
                landmarks['right_ankle']['visibility'] >= MIN_VISIBILITY):

                angle = self._calculate_angle(
                    landmarks['right_hip'],
                    landmarks['right_knee'],
                    landmarks['right_ankle']
                )
                knee_angles.append(angle)

        return {
            'avg_knee_angle': np.mean(knee_angles) if knee_angles else None,
            'min_knee_angle': np.min(knee_angles) if knee_angles else None,
        }

    def _detect_issues(self) -> List[FreestyleIssue]:
        """Detect technique issues based on analyzed metrics."""
        issues = []

        # Check elbow angle
        if self.metrics['elbow']['avg_angle'] is not None:
            avg_elbow = self.metrics['elbow']['avg_angle']
            if avg_elbow > ELBOW_ANGLE_DROPPED:
                issues.append(FreestyleIssue(
                    'dropped_elbow',
                    ISSUE_TYPES['dropped_elbow']['severity'],
                    f"Dropped elbow during catch (avg {avg_elbow:.0f}° - should be {ELBOW_ANGLE_OPTIMAL_MIN}-{ELBOW_ANGLE_OPTIMAL_MAX}°)",
                    ISSUE_TYPES['dropped_elbow']['tip'],
                    avg_elbow
                ))

        # Check body rotation
        if self.metrics['rotation']['avg_rotation'] is not None:
            avg_rotation = self.metrics['rotation']['avg_rotation']
            if avg_rotation < BODY_ROTATION_TOO_FLAT:
                issues.append(FreestyleIssue(
                    'flat_body',
                    ISSUE_TYPES['flat_body']['severity'],
                    f"Limited body rotation ({avg_rotation:.0f}° avg - optimal {BODY_ROTATION_OPTIMAL_MIN}-{BODY_ROTATION_OPTIMAL_MAX}°)",
                    ISSUE_TYPES['flat_body']['tip'],
                    avg_rotation
                ))
            elif avg_rotation > BODY_ROTATION_TOO_MUCH:
                issues.append(FreestyleIssue(
                    'over_rotation',
                    ISSUE_TYPES['over_rotation']['severity'],
                    f"Over-rotation ({avg_rotation:.0f}° avg - optimal {BODY_ROTATION_OPTIMAL_MIN}-{BODY_ROTATION_OPTIMAL_MAX}°)",
                    ISSUE_TYPES['over_rotation']['tip'],
                    avg_rotation
                ))

        # Check arm entry
        if self.metrics['entry']['max_crossing'] is not None:
            max_crossing = self.metrics['entry']['max_crossing']
            if max_crossing > ARM_ENTRY_CENTERLINE_THRESHOLD:
                issues.append(FreestyleIssue(
                    'crossing_centerline',
                    ISSUE_TYPES['crossing_centerline']['severity'],
                    f"Crossing centerline on entry ({max_crossing*100:.0f}% of frame width over center)",
                    ISSUE_TYPES['crossing_centerline']['tip'],
                    max_crossing
                ))

        # Check head position
        if self.metrics['head']['vertical_movement'] is not None:
            if self.metrics['head']['vertical_movement'] > HEAD_LIFT_THRESHOLD:
                issues.append(FreestyleIssue(
                    'head_lifting',
                    ISSUE_TYPES['head_lifting']['severity'],
                    f"Head lifting during breathing ({self.metrics['head']['vertical_movement']*100:.0f}% vertical movement)",
                    ISSUE_TYPES['head_lifting']['tip'],
                    self.metrics['head']['vertical_movement']
                ))

        # Check stroke rate
        if self.metrics['stroke_rate']['spm'] is not None:
            spm = self.metrics['stroke_rate']['spm']
            if spm < STROKE_RATE_OPTIMAL_MIN:
                issues.append(FreestyleIssue(
                    'slow_stroke_rate',
                    ISSUE_TYPES['slow_stroke_rate']['severity'],
                    f"Stroke rate below optimal ({spm:.0f} SPM - optimal {STROKE_RATE_OPTIMAL_MIN}-{STROKE_RATE_OPTIMAL_MAX})",
                    ISSUE_TYPES['slow_stroke_rate']['tip'],
                    spm
                ))
            elif spm > STROKE_RATE_OPTIMAL_MAX:
                issues.append(FreestyleIssue(
                    'fast_stroke_rate',
                    ISSUE_TYPES['fast_stroke_rate']['severity'],
                    f"Stroke rate above optimal ({spm:.0f} SPM - optimal {STROKE_RATE_OPTIMAL_MIN}-{STROKE_RATE_OPTIMAL_MAX})",
                    ISSUE_TYPES['fast_stroke_rate']['tip'],
                    spm
                ))

        # Check kick
        if self.metrics['kick']['avg_knee_angle'] is not None:
            avg_knee = self.metrics['kick']['avg_knee_angle']
            if avg_knee < KNEE_ANGLE_EXCESSIVE_BEND:
                issues.append(FreestyleIssue(
                    'excessive_knee_bend',
                    ISSUE_TYPES['excessive_knee_bend']['severity'],
                    f"Excessive knee bend ({avg_knee:.0f}° - should be near {KNEE_ANGLE_OPTIMAL}°)",
                    ISSUE_TYPES['excessive_knee_bend']['tip'],
                    avg_knee
                ))

        # Sort by severity
        severity_order = {SEVERITY_CRITICAL: 0, SEVERITY_MODERATE: 1, SEVERITY_MINOR: 2}
        issues.sort(key=lambda x: severity_order[x.severity])

        return issues

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
