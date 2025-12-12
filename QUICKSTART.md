# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Test Installation

```bash
python test_installation.py
```

If all tests pass, you're ready to go!

## 3. Analyze Your First Video

```bash
python main.py path/to/your/swimming/video.mp4
```

This will create:
- `video_analyzed.mp4` - Annotated video with pose overlay and metrics
- `video_analyzed_report.txt` - Detailed coaching feedback

## 4. Review Your Results

### Watch the Annotated Video
- Green skeleton overlay shows detected pose
- Angle measurements appear at key joints
- Color coding: Green = good, Orange = needs work, Red = critical issue
- Stats panel in corner shows real-time metrics

### Read the Report
The text report includes:
- **Overall Score**: 1-10 technique rating
- **Critical Issues**: Fix these first for maximum improvement
- **Areas for Improvement**: Secondary focus points
- **Detailed Metrics**: All measured values with optimal ranges
- **Top Priorities**: Ranked list of what to work on

## Common Issues

### "No pose detected"
- Make sure swimmer is clearly visible in frame
- Check that lighting is adequate
- Try filming from a clearer side angle

### Low frame detection rate
- Improve lighting conditions
- Reduce camera shake (use tripod)
- Ensure swimmer doesn't go out of frame

### Inaccurate metrics
- Film from pool deck level, side view
- Keep camera perpendicular to swimming direction
- Capture at least 2-3 complete stroke cycles

## Tips for Better Analysis

1. **Lighting**: Film outdoors in daylight or in well-lit indoor pool
2. **Angle**: Side view, 90° to swimming direction
3. **Stability**: Use tripod or stable surface
4. **Distance**: Far enough to capture full body, close enough for detail
5. **Duration**: At least 10 seconds showing 2-3+ strokes

## Example Command Reference

```bash
# Basic analysis (video + report)
python main.py swim.mp4

# Custom output location
python main.py swim.mp4 -o results/analysis.mp4

# Report only (faster, no video processing)
python main.py swim.mp4 --report-only

# Video only (skip text report)
python main.py swim.mp4 --no-report

# Help
python main.py --help
```

## What to Do With Your Results

1. **Focus on Critical Issues First** (marked with 🔴)
   - These have the biggest impact on efficiency
   - Work on one at a time

2. **Film Regular Check-ins**
   - Record yourself every 2-3 weeks
   - Track improvement over time
   - See if technique changes are sticking

3. **Practice Drills for Each Issue**
   - Dropped elbow → Catch-up drill, fingertip drag drill
   - Flat body → Kick-on-side drill, 6-3-6 drill
   - Crossing centerline → Shoulder-tap drill

4. **Compare Before/After**
   - Save your videos and reports
   - Measure progress objectively
   - Celebrate improvements!

## Need Help?

- Check the full README.md for detailed documentation
- Review example outputs in the examples/ folder (if available)
- Report issues on GitHub

---

Ready to improve your freestyle? Let's go! 🏊‍♂️
