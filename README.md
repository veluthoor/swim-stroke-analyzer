# Swim Stroke Analyzer

AI-powered freestyle swimming technique analysis for distance enthusiasts. Get coaching-quality feedback on your form without a coach.

## Features

- **Pose Detection**: Uses MediaPipe to track your body position throughout the stroke
- **Technique Analysis**: Evaluates key metrics including:
  - Elbow angle during catch phase
  - Body rotation
  - Arm entry position
  - Head stability
  - Kick mechanics
  - Stroke rate
- **Annotated Video**: Visual overlay showing skeleton, angles, and real-time metrics
- **Coaching Feedback**: Actionable tips prioritized by impact on efficiency

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone or download this repository:
```bash
cd swim-stroke-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Analysis

Analyze a swimming video and get both a text report and annotated video:

```bash
python main.py path/to/your/video.mp4
```

This will generate:
- `path/to/your/video_analyzed.mp4` - Annotated video with pose overlay
- `path/to/your/video_analyzed_report.txt` - Detailed text report

### Options

**Custom output path:**
```bash
python main.py video.mp4 -o output/analysis.mp4
```

**Report only (skip video generation):**
```bash
python main.py video.mp4 --report-only
```

**Video only (skip text report):**
```bash
python main.py video.mp4 --no-report
```

### Video Requirements

For best results, your video should:
- Show side view of the swimmer (above water)
- Have good lighting
- Be stable (not shaky)
- Show at least 2-3 complete stroke cycles
- Capture the full body when possible

**Supported formats:** MP4, AVI, MOV

## Understanding Your Results

### Sample Report

```
FREESTYLE STROKE ANALYSIS
============================================================

Overall Technique Score: 7/10

🔴 Critical Issues:
------------------------------------------------------------

• Dropped elbow during catch (avg 130° - should be 80-100°)
  → Focus on high elbow catch. Imagine reaching over a barrel.

🟡 Areas for Improvement:
------------------------------------------------------------

• Limited body rotation (35° avg - optimal 45-60°)
  → Increase rotation from hips. Roll your body like a log.

⚡ DETAILED METRICS
------------------------------------------------------------
Elbow Angle:
  Average: 130.2° (optimal: 80-100°)
  Left: 128.5° | Right: 132.1°

Body Rotation:
  Average: 35.4° (optimal: 45-60°)

Stroke Rate:
  52.3 strokes per minute (optimal: 50-60 SPM)

🎯 TOP PRIORITIES
------------------------------------------------------------
1. Fix dropped elbow
2. Increase body rotation
```

### Metrics Explained

**Elbow Angle (80-100° optimal)**
- Measured at the catch phase (when hand enters water and begins pull)
- Lower angle = better "high elbow catch" = more efficient pull
- >120° indicates "dropped elbow" - common efficiency killer

**Body Rotation (45-60° optimal)**
- How much you roll from side to side
- Proper rotation reduces drag and improves power
- Too flat (<30°) or over-rotating (>70°) both reduce efficiency

**Stroke Rate (50-60 SPM optimal for distance)**
- Strokes per minute
- Balance between tempo and distance per stroke
- Sprinting uses higher rates, distance uses lower rates with longer glide

**Head Stability**
- Measures vertical head movement
- Should rotate (not lift) to breathe
- Lower movement = better streamlining

**Kick Mechanics**
- Knee angle should be near 170° (almost straight)
- Kick from hips, not knees
- Excessive bend creates drag

## How It Works

1. **Pose Detection**: MediaPipe analyzes each frame to identify 33 body landmarks
2. **Metric Calculation**: Computes angles, positions, and movements throughout the stroke
3. **Issue Detection**: Compares metrics against optimal ranges based on swimming biomechanics
4. **Feedback Generation**: Provides specific, actionable coaching tips prioritized by impact
5. **Visualization**: Overlays skeleton and annotations on the original video

## Limitations

- **Camera Angle**: Currently optimized for side view (above water). Underwater or front views may give less accurate results.
- **Single Swimmer**: Works best with one swimmer clearly visible in frame
- **2D Analysis**: Body rotation and depth metrics are approximations from single camera angle
- **Stroke Detection**: Stroke counting is simplified and may not be 100% accurate
- **Not a Replacement for Coaching**: This tool provides data and suggestions, but working with a real coach is invaluable for personalized feedback

## Roadmap

Future enhancements planned:
- [ ] Support for underwater footage
- [ ] Multiple camera angle fusion
- [ ] Stroke-by-stroke comparison
- [ ] Training progress tracking over time
- [ ] Support for other strokes (backstroke, breaststroke, butterfly)
- [ ] Mobile app version
- [ ] Real-time analysis during swim practice

## Tips for Best Results

1. **Film from the side** at pool deck level
2. **Keep the camera steady** - use a tripod if possible
3. **Ensure good lighting** - outdoor pools in daylight work great
4. **Capture full strokes** - show entry, pull, and recovery
5. **Swim naturally** - don't change your form for the camera
6. **Review multiple videos** over time to track improvement

## Technical Details

**Built with:**
- Python 3.8+
- OpenCV for video processing
- MediaPipe for pose estimation
- NumPy for calculations

**Architecture:**
- `pose_detector.py` - MediaPipe integration
- `stroke_analyzer.py` - Metric calculation and issue detection
- `visualizer.py` - Video annotation and overlay
- `feedback_generator.py` - Report generation
- `models/freestyle_rules.py` - Swimming technique rules and thresholds

## Contributing

This is an early MVP. Feedback, issues, and contributions welcome!

Areas that could use improvement:
- Better stroke cycle detection algorithms
- More sophisticated 3D position estimation
- Expanded coaching knowledge base
- Support for additional camera angles

## License

MIT License - feel free to use and modify for your swimming improvement journey!

## Acknowledgments

Swimming technique guidelines based on coaching principles from:
- Total Immersion Swimming
- USA Swimming technical resources
- Olympic swimming biomechanics research

---

**Built for swimmers, by swimmers. Train smarter, swim faster.** 🏊‍♂️💨
