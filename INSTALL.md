# Installation Guide

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **10-15 minutes** for setup

Check your Python version:
```bash
python3 --version
# Should show: Python 3.8.x or higher
```

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd swim-stroke-analyzer
```

### Step 2: Install Dependencies

```bash
pip3 install -r requirements.txt
```

**What gets installed:**
- `opencv-python` (4.8.0+) - Video processing
- `mediapipe` (0.10.0+) - AI pose detection
- `numpy` (1.24.0+) - Numerical computations

**Installation time:** 2-5 minutes depending on internet speed

**Note for Mac M1/M2 users:**
If you encounter issues, you may need:
```bash
pip3 install --upgrade pip
pip3 install opencv-python mediapipe numpy
```

**Note for Linux users:**
You may need additional system packages:
```bash
sudo apt-get update
sudo apt-get install python3-opencv
pip3 install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python3 test_installation.py
```

**Expected output:**
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
You're ready to analyze swimming videos!

Try: python main.py your_video.mp4
```

If all checks pass ✓, you're ready to go!

## Troubleshooting

### Issue: "pip: command not found"

**Solution:**
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python3 -m pip install -r requirements.txt
```

### Issue: "Permission denied"

**Solution:**
```bash
# Install in user directory
pip3 install --user -r requirements.txt
```

### Issue: MediaPipe installation fails

**Solution for Mac:**
```bash
# Update pip first
pip3 install --upgrade pip

# Try installing mediapipe separately
pip3 install mediapipe

# If still fails, try specific version
pip3 install mediapipe==0.10.8
```

**Solution for Linux:**
```bash
# Install system dependencies
sudo apt-get install python3-dev
sudo apt-get install libopencv-dev

# Then install requirements
pip3 install -r requirements.txt
```

### Issue: Import errors when running

**Solution:**
Make sure you're in the project directory:
```bash
cd swim-stroke-analyzer
python3 main.py video.mp4
```

### Issue: "No module named 'cv2'"

**Solution:**
```bash
# Reinstall opencv-python
pip3 uninstall opencv-python
pip3 install opencv-python
```

## Verifying Components

### Test Python version
```bash
python3 --version
# Need: 3.8 or higher
```

### Test pip
```bash
pip3 --version
# Should show pip version and Python version
```

### Test individual packages
```bash
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import mediapipe; print('MediaPipe: OK')"
python3 -c "import numpy; print('NumPy:', numpy.__version__)"
```

## Virtual Environment (Optional but Recommended)

To avoid conflicts with other Python projects:

```bash
# Create virtual environment
python3 -m venv swim_env

# Activate it (Mac/Linux)
source swim_env/bin/activate

# Activate it (Windows)
swim_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# When done, deactivate
deactivate
```

## First Run

After successful installation:

```bash
# Test with help command
python3 main.py --help

# Should show usage information
```

## System Requirements

**Minimum:**
- Python 3.8+
- 4 GB RAM
- 500 MB disk space

**Recommended:**
- Python 3.10+
- 8 GB RAM
- 2 GB disk space (for videos)
- Webcam or video files to analyze

## Next Steps

✓ Installation complete!

Now read:
1. **QUICKSTART.md** - Get analyzing in 5 minutes
2. **EXAMPLES.md** - See usage examples
3. **README.md** - Full documentation

Or just run:
```bash
python3 main.py your_swim_video.mp4
```

---

**Having issues?** Check:
- Python version is 3.8+
- pip is up to date: `pip3 install --upgrade pip`
- You're in the project directory
- All three packages installed successfully

Still stuck? Review the error messages carefully - they usually point to the problem.
