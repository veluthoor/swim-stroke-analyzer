# Usage Examples

## Getting Started

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_installation.py
```

Expected output:
```
============================================================
SWIM STROKE ANALYZER - INSTALLATION TEST
============================================================

Testing package imports...
  ✓ opencv-python
  ✓ mediapipe
  ✓ numpy

All packages installed correctly!

Testing MediaPipe pose detection...
  ✓ MediaPipe working correctly

Testing OpenCV...
  ✓ OpenCV working correctly
  OpenCV version: 4.8.1

============================================================
SUCCESS! All tests passed.
```

## Basic Usage

### Analyze a Video (Full Analysis)

```bash
python main.py freestyle_pool.mp4
```

**What happens:**
1. Processes video frame by frame
2. Detects swimmer pose in each frame
3. Analyzes technique metrics
4. Generates annotated video
5. Creates text report

**Output files:**
- `freestyle_pool_analyzed.mp4` - Annotated video
- `freestyle_pool_analyzed_report.txt` - Coaching feedback

**Expected runtime:** 2-3 minutes for 30-second video

### Quick Analysis (Report Only)

When you just want the metrics without video processing:

```bash
python main.py freestyle_pool.mp4 --report-only
```

**Faster:** Skips video rendering (~1 minute for 30-sec video)

**Output:** Only creates `freestyle_pool_analyzed_report.txt`

### Video Only (No Report)

When you want the visual analysis without text:

```bash
python main.py freestyle_pool.mp4 --no-report
```

**Output:** Only creates `freestyle_pool_analyzed.mp4`

## Advanced Usage

### Custom Output Location

```bash
# Save to specific directory
python main.py videos/swim1.mp4 -o results/analysis_2024_12_11.mp4

# Different filename
python main.py pool_session.mp4 -o my_technique_check.mp4
```

### Batch Processing

Analyze multiple videos:

```bash
# Using a loop
for video in videos/*.mp4; do
    echo "Processing $video..."
    python main.py "$video"
done
```

Or create a script `batch_analyze.sh`:
```bash
#!/bin/bash
for video in "$@"; do
    echo "Analyzing $video..."
    python main.py "$video" --report-only
done
echo "Batch processing complete!"
```

Run it:
```bash
chmod +x batch_analyze.sh
./batch_analyze.sh video1.mp4 video2.mp4 video3.mp4
```

### Compare Two Sessions

```bash
# Analyze both videos
python main.py before_coaching.mp4 -o results/before.mp4
python main.py after_coaching.mp4 -o results/after.mp4

# Compare the reports manually
diff results/before_analyzed_report.txt results/after_analyzed_report.txt
```

## Real-World Scenarios

### Scenario 1: Weekly Progress Check

```bash
# File naming convention: YYYY-MM-DD_session.mp4
python main.py 2024-12-11_morning.mp4

# Creates:
# - 2024-12-11_morning_analyzed.mp4
# - 2024-12-11_morning_analyzed_report.txt

# Keep these in a folder to track improvement over weeks
```

### Scenario 2: Pre-Competition Assessment

```bash
# Quick check before race
python main.py taper_week.mp4 --report-only

# Read the report
cat taper_week_analyzed_report.txt

# Focus on any new critical issues
```

### Scenario 3: Technique Drill Validation

```bash
# Record before drill
python main.py before_drill.mp4 --report-only

# Practice drill for 10 minutes
# Record after drill

python main.py after_drill.mp4 --report-only

# Compare elbow angles, body rotation, etc.
```

### Scenario 4: Coach Review Session

```bash
# Create full analysis with video
python main.py athlete_freestyle.mp4

# Watch video together
open athlete_freestyle_analyzed.mp4

# Discuss specific frames showing issues
# Use report for objective metrics
```

## Understanding the Output

### Annotated Video Features

When you watch the `*_analyzed.mp4` file, you'll see:

1. **Green Skeleton**: Body pose overlay
2. **Angle Markers**: Numbers showing joint angles
3. **Color Coding**:
   - Green = Good technique
   - Orange = Needs improvement
   - Red = Critical issue
4. **Stats Panel** (top left):
   - Current elbow angle
   - Body rotation
   - Stroke rate
5. **Progress Bar** (bottom): Video timeline

### Report Structure

The `*_report.txt` contains:

```
==========================================================
FREESTYLE STROKE ANALYSIS
==========================================================

Overall Technique Score: X/10

🔴 Critical Issues:
------------------------------------------------------------
[Most important problems to fix]

🟡 Areas for Improvement:
------------------------------------------------------------
[Secondary focus points]

🔵 Minor Suggestions:
------------------------------------------------------------
[Nice-to-have improvements]

⚡ DETAILED METRICS
------------------------------------------------------------
[All measured values with optimal ranges]

🎯 TOP PRIORITIES
------------------------------------------------------------
[Ranked list of what to work on first]
```

## Tips for Best Results

### Video Recording

**Good example:**
```
Camera setup:
- Side view, 90° angle to swimming direction
- Pool deck level (not elevated)
- Stable (tripod or ledge)
- Good lighting (outdoor daylight ideal)
- Distance: 3-5 meters from swimmer
- Duration: 15-30 seconds (3-4 full strokes)
```

**Poor example:**
```
Common mistakes:
- Filming from above (diving board view)
- Front or back angle instead of side
- Too close (body parts cut off)
- Too far (can't see detail)
- Shaky handheld footage
- Dark indoor pool without lights
- Only 1 stroke cycle captured
```

### Improving Detection Accuracy

If you see "Low frame detection rate":

```bash
# Try these filming tips:
# 1. Increase lighting
# 2. Film during daytime (outdoor pool)
# 3. Slow down (make movements more visible)
# 4. Wear contrasting swim suit (vs pool color)
# 5. Keep full body in frame
# 6. Reduce camera shake
```

### Metric Interpretation

**Elbow Angle**
- 80-100° = Excellent high elbow catch
- 100-120° = Acceptable
- 120°+ = Dropped elbow (fix this!)

**Body Rotation**
- 45-60° = Optimal
- 30-45° = Too flat (increase rotation)
- 60-70° = Over-rotating (control it)

**Stroke Rate**
- 50-60 SPM = Good for distance swimming
- 60-70 SPM = Sprint pace
- <50 SPM = Too slow (or great stroke length!)

## Troubleshooting

### "No pose detected"
```bash
# Check video quality
python main.py problem_video.mp4 --report-only

# If still fails, try:
# - Re-record with better angle
# - Increase lighting
# - Ensure swimmer is fully visible
```

### Output video won't play
```bash
# Some players have codec issues
# Convert output format:
ffmpeg -i output_analyzed.mp4 -vcodec h264 output_analyzed_h264.mp4
```

### Processing too slow
```bash
# Use report-only mode for quick checks
python main.py video.mp4 --report-only

# Or trim video to key section first:
ffmpeg -i long_video.mp4 -ss 00:00:10 -t 00:00:20 trimmed.mp4
python main.py trimmed.mp4
```

## Next Steps

After getting your first analysis:

1. **Focus on Top Priority** from report
2. **Look up drill** for that specific issue
3. **Practice drill** for 10-15 minutes
4. **Record again** next session
5. **Compare metrics** to track improvement

Remember: Technique improvement is gradual. Focus on one thing at a time!

---

Need more help? Check `README.md` for detailed documentation.
