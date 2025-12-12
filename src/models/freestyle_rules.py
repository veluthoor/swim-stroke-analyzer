"""Swimming technique rules and thresholds for freestyle stroke analysis."""

# Elbow angle thresholds (degrees)
ELBOW_ANGLE_OPTIMAL_MIN = 80
ELBOW_ANGLE_OPTIMAL_MAX = 100
ELBOW_ANGLE_DROPPED = 120  # Above this is considered "dropped elbow"

# Body rotation thresholds (degrees)
BODY_ROTATION_OPTIMAL_MIN = 45
BODY_ROTATION_OPTIMAL_MAX = 60
BODY_ROTATION_TOO_FLAT = 30  # Below this is too flat
BODY_ROTATION_TOO_MUCH = 70  # Above this is over-rotating

# Arm entry - distance from centerline (pixels - will be normalized)
ARM_ENTRY_CENTERLINE_THRESHOLD = 0.15  # 15% of frame width

# Head position - vertical movement threshold
HEAD_LIFT_THRESHOLD = 0.1  # 10% of frame height variation

# Stroke rate thresholds (strokes per minute)
STROKE_RATE_OPTIMAL_MIN = 50
STROKE_RATE_OPTIMAL_MAX = 60

# Knee angle thresholds (degrees) - should be minimal bend
KNEE_ANGLE_OPTIMAL = 170  # Nearly straight
KNEE_ANGLE_EXCESSIVE_BEND = 140  # Too much bending

# Visibility threshold for landmark confidence
MIN_VISIBILITY = 0.5

# Issue severity levels
SEVERITY_CRITICAL = "critical"
SEVERITY_MODERATE = "moderate"
SEVERITY_MINOR = "minor"


class FreestyleIssue:
    """Represents a detected technique issue."""

    def __init__(self, issue_type: str, severity: str, description: str, tip: str, metric_value=None):
        self.issue_type = issue_type
        self.severity = severity
        self.description = description
        self.tip = tip
        self.metric_value = metric_value

    def __repr__(self):
        return f"FreestyleIssue({self.issue_type}, {self.severity})"


# Issue definitions with coaching tips
ISSUE_TYPES = {
    'dropped_elbow': {
        'name': 'Dropped Elbow',
        'tip': 'Focus on high elbow catch. Imagine reaching over a barrel. Keep your elbow higher than your wrist during the catch phase.',
        'severity': SEVERITY_CRITICAL,
    },
    'flat_body': {
        'name': 'Flat Body Position',
        'tip': 'Increase body rotation (45-60°). Initiate rotation from your hips, not shoulders. Roll your body like a log.',
        'severity': SEVERITY_CRITICAL,
    },
    'over_rotation': {
        'name': 'Over-rotation',
        'tip': 'Reduce body rotation. Focus on controlled roll. Your shoulders should rotate more than your hips.',
        'severity': SEVERITY_MODERATE,
    },
    'crossing_centerline': {
        'name': 'Arm Crossing Centerline',
        'tip': 'Enter your hand in line with your shoulder. Avoid crossing past the centerline of your body. Track straight back.',
        'severity': SEVERITY_CRITICAL,
    },
    'head_lifting': {
        'name': 'Head Lifting During Breathing',
        'tip': 'Rotate your head to breathe, don\'t lift it. Keep one goggle in the water. Look to the side, not forward.',
        'severity': SEVERITY_MODERATE,
    },
    'excessive_knee_bend': {
        'name': 'Excessive Knee Bend',
        'tip': 'Keep your legs straighter. Kick from your hips, not your knees. Small, quick kicks with minimal knee bend.',
        'severity': SEVERITY_MODERATE,
    },
    'slow_stroke_rate': {
        'name': 'Slow Stroke Rate',
        'tip': 'Increase your tempo slightly (aim for 50-60 SPM for distance swimming). Focus on quicker hand turnover.',
        'severity': SEVERITY_MINOR,
    },
    'fast_stroke_rate': {
        'name': 'Fast Stroke Rate',
        'tip': 'Slow down and focus on longer strokes. Glide more after each stroke. Distance per stroke is more efficient.',
        'severity': SEVERITY_MINOR,
    },
}


def get_severity_emoji(severity: str) -> str:
    """Get emoji indicator for severity level."""
    if severity == SEVERITY_CRITICAL:
        return "🔴"
    elif severity == SEVERITY_MODERATE:
        return "🟡"
    else:
        return "🔵"


def get_severity_label(severity: str) -> str:
    """Get text label for severity level."""
    if severity == SEVERITY_CRITICAL:
        return "Critical Issues"
    elif severity == SEVERITY_MODERATE:
        return "Areas for Improvement"
    else:
        return "Minor Suggestions"
