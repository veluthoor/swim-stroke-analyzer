# Swim Stroke Analyzer

AI-powered freestyle swimming technique analysis with a modern web interface. Get coaching-quality feedback on your form without a coach.

🎯 **Upload. Analyze. Improve.** It's that simple.

## ✨ What's New

**v2.0 - Major Web UI Overhaul:**
- 🚀 **2-3x Faster Analysis** - Optimized MediaPipe processing with smart frame skipping
- 🎨 **Beautiful Web Interface** - Modern, fun, and engaging design
- 📹 **Auto-Play Video** - Analyzed videos play automatically in the browser
- 📊 **Smart Results Display** - Quick insights, biggest red flags, and actionable tips
- 🎯 **Prioritized Action Plans** - Know exactly what to fix first
- ✅ **Celebrate Strengths** - See what you're doing well, not just problems
- 💡 **Shareable Reports** - Quick insights perfect for sharing with coaches or teammates

## Features

### Core Analysis
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

### Web Interface
- **Drag & Drop Upload** - Just drop your video and go
- **Real-Time Progress** - Visual step tracker with fun messages
- **Score Display** - Big, beautiful score card (X/10) with emoji feedback
- **Smart Parsing** - Automatically extracts and displays:
  - 📊 Quick Insight - The TL;DR of your swim
  - 🚨 Biggest Red Flag - Top priority issue with fix
  - ✅ What's Working - Your strengths
  - 🎯 Action Plan - Prioritized steps (critical → important)
- **Auto-Play Video** - See your analyzed swim immediately
- **Download Option** - Save the annotated video for later review

## Installation

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** (for web interface)
- **npm** or **yarn**

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd swim-stroke-analyzer
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies:**
```bash
cd frontend
npm install
cd ..
```

4. **Start the application:**

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

5. **Open your browser:**
```
http://localhost:3000
```

That's it! 🎉

## Usage

### Web Interface (Recommended)

1. **Upload**: Drag and drop your swim video (or click to browse)
2. **Wait**: Watch the fun progress messages while AI analyzes your technique
3. **Review**: Get your score, insights, and action plan
4. **Watch**: Auto-play video shows your analyzed swim with overlays
5. **Download**: Save the annotated video if you want
6. **Improve**: Follow the prioritized action plan
7. **Repeat**: Upload another video to track progress!

### Command Line (Advanced)

Analyze a swimming video and get both a text report and annotated video:

```bash
python main.py path/to/your/video.mp4
```

This will generate:
- `path/to/your/video_analyzed.mp4` - Annotated video with pose overlay
- `path/to/your/video_analyzed_report.txt` - Detailed text report

**Options:**

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
- ✅ Show **side view** of the swimmer (above water)
- ✅ Have **good lighting**
- ✅ Be **stable** (not shaky - use a tripod!)
- ✅ Show at least **2-3 complete stroke cycles**
- ✅ Capture the **full body** when possible
- ✅ Be **15-60 seconds** long (sweet spot for analysis)

**Supported formats:** MP4, AVI, MOV

**Tips:**
- Film at pool deck level, not from above
- Outdoor pools in daylight work great
- Keep the swimmer in frame throughout
- Swim naturally - don't change your form for the camera

## Understanding Your Results

### Your Score

You'll get an overall technique score from **1-10**:
- **9-10** 🏆 Olympic-level! Maintain consistency
- **7-8** 🎯 Solid technique! A few tweaks away from pro
- **5-6** 👍 Getting there! Clear areas to improve
- **1-4** 💪 Room to improve! Follow the action plan

### Quick Insight

A shareable one-liner about your swim. Examples:
- *"Solid foundation, but you're losing speed due to dropped elbow. Fix that and you'll see big gains!"*
- *"Your technique is Olympic-level! Maintain this form and focus on consistency."*

### Biggest Red Flag

If you have critical issues, this highlights the #1 problem costing you the most speed/efficiency, plus exactly how to fix it.

### What's Working

We don't just point out problems! This section celebrates your strengths:
- Great elbow catch angle
- Excellent body rotation
- Solid head position
- Optimal stroke rate

### Action Plan

Prioritized list of fixes:
1. **🚨 FIX THIS FIRST** - Critical issues (lose 2 points each)
2. **⚠️ IMPORTANT** - Moderate issues (lose 1 point each)

Each item includes:
- Clear description of the problem
- Specific fix instructions
- Why it matters

### Sample Report

```
🏊‍♂️ YOUR SWIM ANALYSIS

Overall Technique Score: 7/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUICK INSIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 Solid foundation, but you're losing speed/efficiency due to:
dropped elbow. Fix that and you'll see big gains!

🚨 BIGGEST RED FLAG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Dropped elbow during catch (avg 130° - should be 80-100°)

💡 HOW TO FIX IT:
   Focus on high elbow catch. Imagine reaching over a barrel.

✅ WHAT'S WORKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Excellent body rotation - you're using your core effectively!
• Optimal stroke rate - nice rhythm and tempo!

🎯 YOUR ACTION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Focus on these in order:

1. 🚨 FIX THIS FIRST: Dropped elbow during catch
   → Focus on high elbow catch. Imagine reaching over a barrel.

2. ⚠️ IMPORTANT: Head lifting during breathing
   → Rotate head to breathe, don't lift. Keep one eye in water.
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

## Performance

**Analysis Speed:**
- 15-second video: ~1-2 minutes
- 30-second video: ~2-3 minutes
- 60-second video: ~4-6 minutes

**Optimization features:**
- Smart frame skipping (analyzes every 2nd frame)
- Balanced MediaPipe model (complexity=1)
- Efficient video codec (H.264 for browser compatibility)
- Background processing with real-time progress updates

## How It Works

### Analysis Pipeline

1. **Upload** → Video sent to Flask backend
2. **Pose Detection** → MediaPipe analyzes each frame to identify 33 body landmarks
3. **Metric Calculation** → Computes angles, positions, and movements throughout the stroke
4. **Issue Detection** → Compares metrics against optimal ranges based on swimming biomechanics
5. **Feedback Generation** → Creates prioritized, actionable coaching tips
6. **Visualization** → Overlays skeleton and annotations on the original video
7. **Results Display** → React frontend shows beautiful, interactive results

### Tech Stack

**Backend:**
- Python 3.8+ with Flask
- OpenCV for video processing (H.264 codec)
- MediaPipe for pose estimation
- NumPy for calculations

**Frontend:**
- React 18
- Modern CSS with gradients and animations
- Responsive design
- Video auto-play with browser compatibility

**Architecture:**
```
backend/
  app.py                    - Flask REST API
src/
  pose_detector.py          - MediaPipe integration (optimized)
  stroke_analyzer.py        - Metric calculation and issue detection
  visualizer.py             - Video annotation and overlay
  feedback_generator.py     - Report generation (engaging format)
  models/freestyle_rules.py - Swimming technique rules
frontend/
  src/
    App.js                  - Main app with gradient header
    components/
      UploadComponent.js    - Drag & drop upload
      ProcessingComponent.js - Fun progress tracking
      ResultsComponent.js   - Beautiful results display
```

## API Endpoints

**`POST /api/upload`**
- Upload video for analysis
- Returns: `video_id` for tracking

**`GET /api/status/:video_id`**
- Check processing status
- Returns: `status`, `progress`, `message`

**`GET /api/result/:video_id/video`**
- Stream analyzed video (H.264)
- Returns: MP4 video with pose overlays

**`GET /api/result/:video_id/report`**
- Get text report
- Returns: JSON with full report text

**`GET /api/health`**
- Health check
- Returns: `{status: 'ok'}`

## Limitations

- **Camera Angle**: Currently optimized for side view (above water). Underwater or front views may give less accurate results.
- **Single Swimmer**: Works best with one swimmer clearly visible in frame
- **2D Analysis**: Body rotation and depth metrics are approximations from single camera angle
- **Stroke Detection**: Stroke counting is simplified and may not be 100% accurate
- **Not a Replacement for Coaching**: This tool provides data and suggestions, but working with a real coach is invaluable for personalized feedback

## Troubleshooting

**Video won't upload:**
- Check file size (max 500MB)
- Ensure format is MP4, AVI, or MOV
- Try a shorter video (15-60 seconds is ideal)

**Processing stuck:**
- Check backend terminal for errors
- Ensure MediaPipe is installed correctly
- Try restarting both backend and frontend

**Video won't play in browser:**
- This should be fixed in v2.0 (H.264 codec)
- If issues persist, try downloading the video
- Check browser console for errors

**Analysis taking too long:**
- Shorter videos process faster
- Check your system resources
- Normal: 1-2 minutes for 15-second video

## Roadmap

**Near-term:**
- [ ] Stroke-by-stroke breakdown
- [ ] Side-by-side comparison with reference videos
- [ ] Mobile-responsive design improvements
- [ ] Persistent storage for results (currently in-memory)
- [ ] User accounts and progress tracking

**Future enhancements:**
- [ ] Support for underwater footage
- [ ] Multiple camera angle fusion
- [ ] Training progress tracking over time
- [ ] Support for other strokes (backstroke, breaststroke, butterfly)
- [ ] Mobile app version
- [ ] Real-time analysis during swim practice
- [ ] Social sharing features
- [ ] Leaderboards and challenges

## Contributing

This project is actively being improved! Feedback, issues, and contributions welcome.

**Areas that could use help:**
- Better stroke cycle detection algorithms
- More sophisticated 3D position estimation
- Expanded coaching knowledge base
- Support for additional camera angles
- Mobile app development
- UI/UX improvements

## License

MIT License - feel free to use and modify for your swimming improvement journey!

## Acknowledgments

**Swimming technique guidelines based on:**
- Total Immersion Swimming
- USA Swimming technical resources
- Olympic swimming biomechanics research

**Technology:**
- MediaPipe by Google
- OpenCV
- React
- Flask

---

**Built for swimmers, by swimmers. Train smarter, swim faster.** 🏊‍♂️💨

**Try it now:** Upload a video and get coaching-quality feedback in minutes!

---

## Author

**Charu Veluthoor**

I built this tool because I've wanted to fix my swim form for ages, but coaches haven't been the most accessible. I've constantly recorded videos and tried sending them around to coaches since I work in the industry, but I realized others don't have this luxury—and how great it would be to have a coach on call, available whenever you need feedback.

So I built this for myself and for everyone else on this swimming journey.

This tool is constantly a work in progress and is being continuously reviewed and improved by swimmers and swim coaches. Whether you're training for your first triathlon, working on distance efficiency, or just want to swim better, this is for you.

**All feedback welcome!** Open an issue, suggest improvements, or share your swimming journey. Let's make this better together. 🏊‍♂️

Built with ❤️ for swimmers, by a swimmer.
