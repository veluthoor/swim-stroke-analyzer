# How to Test the Swim Stroke Analyzer

## ✅ Installation Complete!

Your installation is verified and working. All dependencies are installed correctly.

## 🎬 Getting a Test Video

You need a swimming video to analyze. Here are your options:

### Option 1: Use Your Own Video (Recommended)

**Record yourself or a friend swimming freestyle:**
- 📹 Film from the side (pool deck level)
- ⏱️ 15-30 seconds
- 🏊‍♂️ Show 2-3 complete stroke cycles
- 🌞 Good lighting
- 📱 Phone camera is fine!

**Transfer to this folder:**
```bash
# Copy your video here
cp /path/to/your/swim_video.mp4 ~/swim-stroke-analyzer/
```

### Option 2: Download from YouTube

Use `yt-dlp` or similar to download a freestyle swimming video:

```bash
# Install yt-dlp (if you don't have it)
brew install yt-dlp  # or: pip3 install yt-dlp

# Download a video (example - find a freestyle technique video)
yt-dlp "https://www.youtube.com/watch?v=FREESTYLE_VIDEO_ID" -o swim_test.mp4
```

**Good search terms:**
- "freestyle swimming side view"
- "freestyle technique demonstration"
- "swimming pool side view"

### Option 3: Use Sample Footage

Search for "freestyle swimming stock footage" or check these sources:
- Pexels.com (free stock videos)
- Pixabay.com (free videos)
- Coverr.co (free videos)

Look for videos with:
- ✅ Side view angle
- ✅ Above water
- ✅ Clear swimmer visibility
- ✅ Freestyle stroke

## 🚀 Running Your First Analysis

Once you have a video (let's say it's called `swim_test.mp4`):

```bash
# Navigate to project
cd ~/swim-stroke-analyzer

# Run analysis
python3 main.py swim_test.mp4
```

**What happens:**
1. Processes video frame by frame (~2-3 minutes)
2. Detects swimmer's pose using AI
3. Calculates technique metrics
4. Creates annotated video
5. Generates coaching report

**Output files created:**
- `swim_test_analyzed.mp4` - Video with skeleton overlay and metrics
- `swim_test_analyzed_report.txt` - Detailed coaching feedback

## 📺 View Results

```bash
# Watch the annotated video
open swim_test_analyzed.mp4

# Read the text report
cat swim_test_analyzed_report.txt

# Or open in text editor
open swim_test_analyzed_report.txt
```

## 🧪 Quick Demo Test

If you don't have a swimming video yet, you can test the system with ANY video of a person moving:

```bash
# Test with any video (won't give swimming analysis, but proves system works)
python3 main.py /path/to/any/video/with/person.mp4 --report-only
```

This will show you the system is working, even if the metrics won't be meaningful for non-swimming videos.

## 📋 Expected Output Example

When running on a real swimming video, you'll see:

```
============================================================
SWIM STROKE ANALYZER
============================================================
Input video: swim_test.mp4
Output video: swim_test_analyzed.mp4

Step 1/4: Detecting pose in video frames...
Processing video: 900 frames at 30.00 fps
Processed 30/900 frames
Processed 60/900 frames
...
Completed: 900 frames processed
✓ Processed 900 frames

Step 2/4: Analyzing stroke mechanics...

Analyzing stroke mechanics...
Valid frames: 850/900
✓ Analysis complete

Step 3/4: Generating feedback report...
✓ Report generated

============================================================
FREESTYLE STROKE ANALYSIS
============================================================

Overall Technique Score: 7/10

🔴 Critical Issues:
------------------------------------------------------------

• Dropped elbow during catch (avg 125° - should be 80-100°)
  → Focus on high elbow catch. Imagine reaching over a barrel.

...

Step 4/4: Creating annotated video...

Creating annotated video...
Rendered 30/900 frames
...
Completed: swim_test_analyzed.mp4
✓ Video saved to: swim_test_analyzed.mp4

============================================================
ANALYSIS COMPLETE
============================================================
Score: 7/10 | Critical Issues: 2 | Areas for Improvement: 1
```

## 🎯 What to Look For

### In the Annotated Video:
- **Green skeleton** overlay tracking the swimmer
- **Angle measurements** at key joints (elbows, knees)
- **Color coding**: Green (good), Orange (needs work), Red (critical)
- **Stats panel** in top-left corner
- **Progress bar** at bottom

### In the Text Report:
- **Overall score** (1-10)
- **Critical issues** (🔴) - Fix these first!
- **Moderate issues** (🟡) - Work on these next
- **Detailed metrics** - All measurements
- **Coaching tips** - Specific advice for each issue

## ❓ Troubleshooting

### "No valid pose data detected"
- Video quality might be poor
- Try a different video with clearer swimmer visibility
- Ensure good lighting in the video

### Takes too long?
```bash
# Use report-only mode (skips video rendering, much faster)
python3 main.py video.mp4 --report-only
```

### Want to analyze multiple videos?
```bash
# Create output folder
mkdir results

# Analyze multiple videos
python3 main.py video1.mp4 -o results/video1_analyzed.mp4
python3 main.py video2.mp4 -o results/video2_analyzed.mp4
```

## 🎓 Next Steps

Once you've tested it:

1. **Record your own swimming** (or a friend's)
2. **Analyze the video**
3. **Review the feedback**
4. **Work on top priorities**
5. **Record again** in 1-2 weeks
6. **Track improvement** over time!

## 📞 Need Help?

If you're stuck:
1. Make sure you have a video file in the directory
2. Check video is a supported format (MP4, AVI, MOV)
3. Run `python3 test_installation.py` again to verify setup
4. Try with `--report-only` flag first (faster test)

---

**Ready to test?** Get a swimming video and run:
```bash
python3 main.py your_video.mp4
```

Good luck! 🏊‍♂️💨
