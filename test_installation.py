#!/usr/bin/env python3
"""Test script to verify installation and dependencies."""

import sys


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")

    packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
    }

    failed = []

    for package, pip_name in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {pip_name}")
        except ImportError:
            print(f"  ✗ {pip_name} - NOT FOUND")
            failed.append(pip_name)

    if failed:
        print(f"\nMissing packages: {', '.join(failed)}")
        print("Install with: pip install " + " ".join(failed))
        return False

    print("\nAll packages installed correctly!")
    return True


def test_mediapipe():
    """Test MediaPipe pose detection."""
    print("\nTesting MediaPipe pose detection...")

    try:
        import mediapipe as mp
        import numpy as np

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        # Create a dummy image
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Try to process it
        results = pose.process(dummy_image)

        pose.close()

        print("  ✓ MediaPipe working correctly")
        return True

    except Exception as e:
        print(f"  ✗ MediaPipe test failed: {e}")
        return False


def test_opencv():
    """Test OpenCV functionality."""
    print("\nTesting OpenCV...")

    try:
        import cv2
        import numpy as np

        # Create a test image
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test basic operations
        cv2.putText(img, "Test", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        print("  ✓ OpenCV working correctly")
        print(f"  OpenCV version: {cv2.__version__}")
        return True

    except Exception as e:
        print(f"  ✗ OpenCV test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("SWIM STROKE ANALYZER - INSTALLATION TEST")
    print("=" * 60)
    print()

    results = []

    results.append(test_imports())
    results.append(test_mediapipe())
    results.append(test_opencv())

    print()
    print("=" * 60)

    if all(results):
        print("SUCCESS! All tests passed.")
        print("You're ready to analyze swimming videos!")
        print()
        print("Try: python main.py your_video.mp4")
        return 0
    else:
        print("FAILED! Some tests did not pass.")
        print("Please check the errors above and fix any issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
