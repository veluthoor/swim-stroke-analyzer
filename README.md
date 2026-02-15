---
title: Swim Stroke Analyzer
emoji: 🏊
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Swim Stroke Analyzer

**Your AI swimming coach, available 24/7.**

I built this because I've wanted to fix my swim form for ages, but coaches haven't been the most accessible. I've constantly recorded videos and tried sending them around to coaches since I work in the industry, but I realized most swimmers don't have this luxury.

So I asked myself: **What if everyone could have a coach on call, available whenever they need feedback?**

That's what this is. Upload your swim video, get coaching-quality feedback in minutes. No scheduling, no commute to the pool, no waiting for email responses. Just you, your video, and instant analysis.

🎯 **Upload. Analyze. Improve.** It's that simple.

---

## ✨ What's New in v2.0

I've been listening to feedback from swimmers and coaches, and here's what's improved:

- 🚀 **2-3x Faster Analysis** - Optimized the AI so you're not waiting forever
- 📊 **Real Insights, Not Data Dumps** - Quick insights, biggest issues, what's working
- 💡 **Shareable Reports** - Perfect for sending to your coach or training partners

---

## Why This Exists

**The Problem:**
You want to improve your swimming, but:
- Coaches are expensive or hard to access
- You can film yourself, but can't see what you're doing wrong
- Asking for feedback means waiting days (or never hearing back)
- You don't know if you're fixing the right things

**The Solution:**
Upload a video. Get immediate, specific, actionable feedback on:
- What's costing you the most speed/efficiency
- Exactly how to fix it
- What you're doing well (yes, there's good stuff too!)
- A prioritized plan so you're not overwhelmed

No BS. No jargon. Just "here's what's wrong and here's how to fix it."

---

## Features

### The Analysis
- **Pose Detection** - AI tracks your body position throughout each stroke
- **Technique Scoring** - Get a 1-10 score (no sugar-coating)
- **Issue Detection** - Analyzes:
  - Elbow angle during catch (the #1 efficiency killer)
  - Body rotation (are you swimming flat?)
  - Head position (are you lifting to breathe?)
  - Kick mechanics (knees vs hips)
  - Stroke rate (tempo optimization)
- **Annotated Video** - See the skeleton overlay, angles, metrics in real-time
- **Coaching Tips** - Specific fixes, prioritized by impact

### The Interface
- **Drag & Drop** - Just drop your video and go
- **Progress Tracking** - Fun messages while you wait (I promise, it's not boring)
- **Score Display** - Big, beautiful score card with emoji feedback
- **Smart Results** - Auto-extracts:
  - 📊 **Quick Insight** - The TL;DR of your swim
  - 🚨 **Biggest Red Flag** - What's hurting you most + how to fix it
  - ✅ **What's Working** - Your strengths
  - 🎯 **Action Plan** - Do this first, then this, then this
- **Auto-Play Video** - Watch your analyzed swim with overlays
- **Download Option** - Save it for later

---

## Getting Started

### What You Need
- Python 3.8+
- Node.js 14+ (for the web interface)
- A video of you swimming (15-60 seconds is perfect)

### Installation

**1. Clone this repo:**
```bash
git clone https://github.com/veluthoor/swim-stroke-analyzer.git
cd swim-stroke-analyzer
```

**2. Install Python stuff:**
```bash
pip install -r requirements.txt
```

**3. Install frontend stuff:**
```bash
cd frontend
npm install
cd ..
```

**4. Start it up:**

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

**5. Open your browser:**
```
http://localhost:3000
```

**That's it!** 🎉

---

## How to Use It

1. **Film yourself swimming** (side view, 15-60 seconds)
2. **Drop the video** into the web interface
3. **Wait 1-2 minutes** while AI does its thing
4. **Get your results:**
   - Overall score (1-10)
   - Biggest issue + how to fix it
   - What you're doing well
   - Prioritized action plan
5. **Watch the video** with AI overlays showing angles, form, etc.
6. **Go practice** and fix the top issue
7. **Upload again** next week to track progress

**Pro tip:** Focus on ONE issue at a time. Trying to fix everything at once = fixing nothing.

---

## What Makes a Good Video?

✅ **Do this:**
- Film from the **side** (pool deck level)
- Use good **lighting** (outdoor pools in daylight = perfect)
- Keep the camera **steady** (tripod helps)
- Show **full body** when possible
- Capture **2-3 complete strokes**
- Swim **naturally** (don't change your form for the camera)

❌ **Avoid:**
- Filming from above or underwater (coming soon!)
- Shaky camera work
- Poor lighting
- Videos shorter than 10 seconds

**Formats:** MP4, AVI, MOV (max 500MB)

---

## Understanding Your Results

### Your Score (1-10)

- **9-10** 🏆 Olympic-level! Keep it consistent
- **7-8** 🎯 Solid form, minor tweaks needed
- **5-6** 👍 Good foundation, clear areas to improve
- **1-4** 💪 Lots of room to grow (that's okay!)

### Quick Insight

One sentence that sums up your swim. Examples:

> *"Solid foundation, but you're losing speed due to dropped elbow. Fix that and you'll see big gains!"*

> *"Your technique is Olympic-level! Maintain this form and focus on consistency."*

### Biggest Red Flag 🚨

If you have critical issues, this highlights **the #1 thing** costing you speed/efficiency, plus exactly how to fix it.

**Why just one?** Because trying to fix 5 things at once means you fix nothing. Master one thing, then move to the next.

### What's Working ✅

You're not doing everything wrong! This celebrates your strengths:
- Great elbow catch angle
- Excellent body rotation
- Solid head position
- Optimal stroke rate

**Why this matters:** Knowing what's working helps you not accidentally break it while fixing other stuff.

### Action Plan 🎯

Prioritized list:
1. **🚨 FIX THIS FIRST** - Critical issues (each costs you 2 points)
2. **⚠️ IMPORTANT** - Moderate issues (each costs you 1 point)

Each includes:
- What's wrong
- How to fix it
- Why it matters

### Sample Report

```
🏊‍♂️ YOUR SWIM ANALYSIS

Overall Technique Score: 7/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUICK INSIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 Solid foundation, but you're losing speed due to dropped
elbow. Fix that and you'll see big gains!

🚨 BIGGEST RED FLAG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Dropped elbow during catch (avg 130° - should be 80-100°)

💡 HOW TO FIX IT:
   Focus on high elbow catch. Imagine reaching over a barrel.
   Practice this drill: Catch-up drill focusing on elbow position.

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

---

## The Metrics Explained (Without the Jargon)

**Elbow Angle (80-100° is optimal)**
- Measured when your hand enters and begins the pull
- Lower angle = "high elbow catch" = more power, less drag
- >120° = "dropped elbow" = you're pushing water down instead of back
- **Fix:** Imagine reaching over a barrel during the catch

**Body Rotation (45-60° is optimal)**
- How much you roll side-to-side
- Proper rotation = less drag + more power from your core
- Swimming flat (<30°) or over-rotating (>70°) both slow you down
- **Fix:** Rotate from the hips, not the shoulders

**Stroke Rate (50-60 SPM for distance)**
- How many strokes per minute
- Higher rate = sprinting, lower rate = distance/efficiency
- Sweet spot depends on your goals
- **Fix:** Film yourself counting strokes, then adjust tempo

**Head Position**
- Should rotate with your body to breathe (not lift)
- Lifting = drag + messed up body position
- **Fix:** Keep one goggle in the water when breathing

**Kick**
- Should come from hips with nearly straight legs (170° knee angle)
- Kicking from knees = drag + wasted energy
- **Fix:** Think "loose ankles, straight legs" from the hip

---

## Performance (How Long Does This Take?)

- **15-second video:** ~1-2 minutes
- **30-second video:** ~2-3 minutes
- **60-second video:** ~4-6 minutes

---

## How It Actually Works

**Behind the scenes:**

1. **Upload** → Video goes to the backend
2. **Pose Detection** → AI (MediaPipe) identifies 33 body points per frame
3. **Metric Calculation** → Computes angles, positions, movement patterns
4. **Issue Detection** → Compares your metrics to optimal ranges
5. **Feedback Generation** → Creates prioritized, actionable tips
6. **Video Creation** → Overlays skeleton, angles, metrics on your video
7. **Results Display** → Frontend shows it beautifully

**Tech stack:**
- **Backend:** Python, Flask, OpenCV, MediaPipe
- **Frontend:** React, modern CSS
- **Video:** H.264 codec (browser-compatible)

---

## Limitations (Being Honest Here)

- **Camera angle:** Currently works best with side view above water. Underwater/front view coming soon.
- **Single swimmer:** Works best when you're the only person clearly visible
- **2D analysis:** Body rotation estimates are approximations (3D would need multiple cameras)
- **Not perfect:** Stroke counting is simplified, may not be 100% accurate
- **Not a replacement for coaching:** This gives you data and direction. A real coach is still invaluable for personalized feedback and accountability.

---

## Troubleshooting

**Video won't upload?**
- Check file size (max 500MB)
- Make sure it's MP4, AVI, or MOV
- Try a shorter clip (15-60 seconds)

**Processing taking forever?**
- Shorter videos = faster processing
- Normal: 1-2 minutes for 15 seconds
- Check backend terminal for errors

**Results seem off?**
- Make sure the camera angle is from the side
- Check that lighting is good
- Ensure you're clearly visible throughout
- Try filming a different angle

---

## Roadmap (What's Coming)

**Soon:**
- [ ] Stroke-by-stroke breakdown
- [ ] Compare your video side-by-side with pros
- [ ] Mobile-friendly design
- [ ] Save your results (currently in-memory only)
- [ ] Track progress over time

**Eventually:**
- [ ] Underwater footage support
- [ ] Multiple camera angles
- [ ] Other strokes (backstroke, breaststroke, butterfly)
- [ ] Mobile app
- [ ] Social features (share with coaches/teammates)
- [ ] Challenges and leaderboards

---

## Want to Help?

This tool is constantly being reviewed and improved by swimmers and swim coaches. **All feedback welcome!**

**Ways to contribute:**
- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Suggest it
- 🏊‍♂️ Are you a swim coach? I'd love your input on the analysis
- 💻 Want to code? PRs welcome
- 📹 Got interesting test videos? Share them

**Areas that need work:**
- Better stroke cycle detection
- 3D position estimation
- More coaching knowledge
- Support for other strokes
- Mobile app

---

## API Endpoints (For Developers)

**`POST /api/upload`**
- Upload video
- Returns: `video_id`

**`GET /api/status/:video_id`**
- Check progress
- Returns: `status`, `progress`, `message`

**`GET /api/result/:video_id/video`**
- Stream analyzed video
- Returns: MP4 with overlays

**`GET /api/result/:video_id/report`**
- Get text report
- Returns: JSON with full analysis

**`GET /api/health`**
- Health check
- Returns: `{status: 'ok'}`

---

## Command Line Usage (For the Nerds)

If you prefer terminal over web interface:

```bash
# Basic analysis
python main.py path/to/video.mp4

# Custom output path
python main.py video.mp4 -o output/analysis.mp4

# Report only (skip video)
python main.py video.mp4 --report-only

# Video only (skip report)
python main.py video.mp4 --no-report
```

---

## License

MIT License - Use it, modify it, improve it. Just give credit where it's due.

---

## Acknowledgments

**Swimming knowledge from:**
- Total Immersion Swimming
- USA Swimming
- Olympic biomechanics research
- Countless coaches and swimmers who've given feedback

**Tech powered by:**
- MediaPipe (Google)
- OpenCV
- React
- Flask

---

## About Me

**Charu Veluthoor**

I'm a swimmer who got tired of not having access to quality coaching feedback. I work in tech and have some industry connections, so I could send videos to coaches—but most people can't do that. It didn't seem fair.

So I built this. For me, and for you, and for everyone else trying to get better at swimming without breaking the bank or waiting weeks for feedback.

This is a living project. Swimmers and coaches are constantly reviewing it, suggesting improvements, and helping make it better. It's not perfect, but it's getting better every day.

**Let's improve together.** Whether you're training for your first triathlon, working on distance efficiency, or just want to swim better—this is for you.

Open an issue, share your story, send feedback. Let's make swimming more accessible for everyone. 🏊‍♂️

---

**Built with ❤️ for swimmers, by a swimmer.**

**Try it now:** Upload a video and get coaching-quality feedback in minutes!
