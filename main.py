#!/usr/bin/env python3
"""
Swim Stroke Analyzer - Main CLI Entry Point

Analyzes freestyle swimming technique from video and provides coaching feedback.
"""

import argparse
import sys
import os
from pathlib import Path

from src.pose_detector import PoseDetector
from src.video_processor import VideoProcessor
from src.stroke_analyzer import StrokeAnalyzer
from src.visualizer import Visualizer
from src.feedback_generator import FeedbackGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze freestyle swimming technique from video',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a video and generate report + annotated video
  python main.py video.mp4

  # Specify custom output path
  python main.py video.mp4 -o output/analysis.mp4

  # Generate report only (no video output)
  python main.py video.mp4 --report-only
        """
    )

    parser.add_argument(
        'video',
        help='Path to input video file'
    )

    parser.add_argument(
        '-o', '--output',
        help='Path for output video (default: input_analyzed.mp4)',
        default=None
    )

    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate text report only, skip video visualization'
    )

    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip text report, only generate annotated video'
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        sys.exit(1)

    # Set output path
    if args.output is None:
        args.output = VideoProcessor.generate_output_path(args.video)

    print("=" * 60)
    print("SWIM STROKE ANALYZER")
    print("=" * 60)
    print(f"Input video: {args.video}")
    if not args.report_only:
        print(f"Output video: {args.output}")
    print("")

    try:
        # Step 1: Extract pose data from video
        print("Step 1/4: Detecting pose in video frames...")
        detector = PoseDetector()
        pose_data = detector.process_video(args.video)

        if not pose_data:
            print("Error: Failed to process video")
            sys.exit(1)

        print(f"✓ Processed {len(pose_data)} frames")
        print("")

        # Step 2: Analyze stroke mechanics
        print("Step 2/4: Analyzing stroke mechanics...")
        analyzer = StrokeAnalyzer()
        analysis_results = analyzer.analyze_video(pose_data)

        if 'error' in analysis_results:
            print(f"Error: {analysis_results['error']}")
            sys.exit(1)

        print("✓ Analysis complete")
        print("")

        # Step 3: Generate feedback report
        if not args.no_report:
            print("Step 3/4: Generating feedback report...")
            feedback = FeedbackGenerator()
            report = feedback.generate_report(analysis_results)
            print("✓ Report generated")
            print("")
            print(report)
            print("")

            # Save report to file
            report_path = args.output.replace('.mp4', '_report.txt')
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"Report saved to: {report_path}")
            print("")
        else:
            print("Step 3/4: Skipping report generation")
            print("")

        # Step 4: Create annotated video
        if not args.report_only:
            print("Step 4/4: Creating annotated video...")
            visualizer = Visualizer()
            output_video = visualizer.create_annotated_video(
                pose_data,
                args.output,
                analysis_results,
                args.video
            )
            print(f"✓ Video saved to: {output_video}")
            print("")
        else:
            print("Step 4/4: Skipping video generation")
            print("")

        print("=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

        # Quick summary
        feedback = FeedbackGenerator()
        summary = feedback.generate_summary(analysis_results)
        print(summary)
        print("")

    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
