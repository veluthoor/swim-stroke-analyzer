# Project Structure

```
swim-stroke-analyzer/
│
├── main.py                          # CLI entry point
├── test_installation.py             # Installation verification script
├── requirements.txt                 # Python dependencies
│
├── README.md                        # Full documentation
├── QUICKSTART.md                    # Quick start guide
├── PROJECT_STRUCTURE.md            # This file
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── pose_detector.py            # MediaPipe pose detection
│   ├── video_processor.py          # Video I/O handling
│   ├── stroke_analyzer.py          # Metrics calculation & issue detection
│   ├── visualizer.py               # Video annotation
│   ├── feedback_generator.py       # Report generation
│   │
│   └── models/                     # Data models
│       ├── __init__.py
│       └── freestyle_rules.py      # Swimming technique rules
│
├── tests/                          # Unit tests (TODO)
├── examples/                       # Example videos (add your own)
└── output/                         # Analysis outputs (auto-created)
```

## Key Components

### Core Modules

**`pose_detector.py`**
- Uses MediaPipe to detect body pose in each frame
- Extracts 33 body landmarks with (x, y, z) coordinates
- Provides utility functions for angle calculations

**`stroke_analyzer.py`**
- Analyzes pose data across entire video
- Calculates key metrics: elbow angles, body rotation, stroke rate, etc.
- Detects technique issues based on swimming biomechanics

**`visualizer.py`**
- Overlays skeleton and annotations on video
- Color-codes metrics (green/orange/red)
- Displays real-time stats panel

**`feedback_generator.py`**
- Generates human-readable coaching feedback
- Prioritizes issues by severity and impact
- Provides actionable tips for each problem

**`video_processor.py`**
- Handles video file I/O
- Manages video properties (fps, dimensions, etc.)
- Creates output video writers

### Models

**`freestyle_rules.py`**
- Defines optimal ranges for all metrics
- Contains issue type definitions
- Provides coaching tips for each common problem
- Configurable thresholds

## Data Flow

```
Input Video
    ↓
[pose_detector.py] → Extract pose data from each frame
    ↓
[stroke_analyzer.py] → Calculate metrics & detect issues
    ↓
    ├─→ [feedback_generator.py] → Generate text report
    └─→ [visualizer.py] → Create annotated video
    ↓
Outputs: analyzed_video.mp4 + report.txt
```

## Adding New Features

### To add a new metric:

1. Add calculation method in `stroke_analyzer.py`
2. Define thresholds in `models/freestyle_rules.py`
3. Add issue detection logic in `_detect_issues()`
4. Add visualization in `visualizer.py` (optional)
5. Update report formatting in `feedback_generator.py`

### To add a new stroke type:

1. Create `models/backstroke_rules.py` (or breaststroke, butterfly)
2. Create `backstroke_analyzer.py` with stroke-specific logic
3. Update `main.py` to accept stroke type argument
4. Add stroke-specific landmark tracking as needed

### To support underwater footage:

1. Adjust pose detection confidence thresholds
2. Add water refraction compensation
3. Update visualization colors for underwater visibility
4. Modify metric calculations for different viewing angle

## Configuration

Key parameters can be adjusted in `models/freestyle_rules.py`:

- **Angle thresholds**: Optimal ranges for elbow, knee, rotation
- **Visibility threshold**: Minimum confidence for landmark detection
- **Stroke rate ranges**: Optimal SPM for different swim styles
- **Issue severity levels**: Critical vs moderate vs minor

## Testing

Run installation test:
```bash
python test_installation.py
```

Future unit tests will go in `tests/` directory.

## Output Files

When you run analysis on `video.mp4`, you'll get:

- `video_analyzed.mp4` - Annotated video with overlays
- `video_analyzed_report.txt` - Detailed text report

These are saved in the same directory as input by default.
