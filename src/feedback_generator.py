"""Generates human-readable feedback reports from analysis results."""

from typing import Dict, List
from src.models.freestyle_rules import (
    FreestyleIssue,
    get_severity_emoji,
    get_severity_label,
    SEVERITY_CRITICAL,
    SEVERITY_MODERATE,
    SEVERITY_MINOR
)


class FeedbackGenerator:
    """Generates structured feedback reports for swimmers."""

    def generate_report(self, analysis_results: Dict) -> str:
        """
        Generate comprehensive text report.

        Args:
            analysis_results: Results from stroke analyzer

        Returns:
            Formatted text report
        """
        metrics = analysis_results['metrics']
        issues = analysis_results['issues']

        report = []
        report.append("=" * 60)
        report.append("FREESTYLE STROKE ANALYSIS")
        report.append("=" * 60)
        report.append("")

        # Overall rating
        rating = self._calculate_overall_rating(issues)
        report.append(f"Overall Technique Score: {rating}/10")
        report.append("")

        # Group issues by severity
        critical_issues = [i for i in issues if i.severity == SEVERITY_CRITICAL]
        moderate_issues = [i for i in issues if i.severity == SEVERITY_MODERATE]
        minor_issues = [i for i in issues if i.severity == SEVERITY_MINOR]

        # Critical issues
        if critical_issues:
            report.append(f"{get_severity_emoji(SEVERITY_CRITICAL)} {get_severity_label(SEVERITY_CRITICAL)}:")
            report.append("-" * 60)
            for issue in critical_issues:
                report.append(f"\n• {issue.description}")
                report.append(f"  → {issue.tip}")
            report.append("")

        # Moderate issues
        if moderate_issues:
            report.append(f"{get_severity_emoji(SEVERITY_MODERATE)} {get_severity_label(SEVERITY_MODERATE)}:")
            report.append("-" * 60)
            for issue in moderate_issues:
                report.append(f"\n• {issue.description}")
                report.append(f"  → {issue.tip}")
            report.append("")

        # Minor issues
        if minor_issues:
            report.append(f"{get_severity_emoji(SEVERITY_MINOR)} {get_severity_label(SEVERITY_MINOR)}:")
            report.append("-" * 60)
            for issue in minor_issues:
                report.append(f"\n• {issue.description}")
                report.append(f"  → {issue.tip}")
            report.append("")

        # No issues found
        if not issues:
            report.append("✅ No major technique issues detected!")
            report.append("Your freestyle form looks solid. Keep up the great work!")
            report.append("")

        # Detailed metrics
        report.append("⚡ DETAILED METRICS")
        report.append("-" * 60)
        report.append(self._format_metrics(metrics))
        report.append("")

        # Priorities
        if critical_issues:
            report.append("🎯 TOP PRIORITIES")
            report.append("-" * 60)
            report.append("Focus on fixing critical issues first for maximum improvement:")
            for i, issue in enumerate(critical_issues[:3], 1):  # Top 3
                report.append(f"{i}. {issue.issue_type.replace('_', ' ').title()}")
            report.append("")

        report.append("=" * 60)
        report.append("💡 Remember: Technique improvements take time and practice.")
        report.append("   Focus on one or two issues at a time for best results.")
        report.append("=" * 60)

        return "\n".join(report)

    def generate_summary(self, analysis_results: Dict) -> str:
        """
        Generate brief summary.

        Args:
            analysis_results: Results from stroke analyzer

        Returns:
            Brief text summary
        """
        issues = analysis_results['issues']
        rating = self._calculate_overall_rating(issues)

        critical_count = len([i for i in issues if i.severity == SEVERITY_CRITICAL])
        moderate_count = len([i for i in issues if i.severity == SEVERITY_MODERATE])

        summary = [
            f"Score: {rating}/10",
            f"Critical Issues: {critical_count}",
            f"Areas for Improvement: {moderate_count}"
        ]

        return " | ".join(summary)

    def _calculate_overall_rating(self, issues: List[FreestyleIssue]) -> int:
        """
        Calculate overall technique rating (1-10).

        Args:
            issues: List of detected issues

        Returns:
            Rating from 1-10
        """
        # Start with perfect score
        score = 10

        # Deduct points based on severity
        for issue in issues:
            if issue.severity == SEVERITY_CRITICAL:
                score -= 2
            elif issue.severity == SEVERITY_MODERATE:
                score -= 1
            elif issue.severity == SEVERITY_MINOR:
                score -= 0.5

        return max(1, min(10, int(round(score))))

    def _format_metrics(self, metrics: Dict) -> str:
        """Format metrics section."""
        lines = []

        # Elbow metrics
        if metrics.get('elbow', {}).get('avg_angle') is not None:
            elbow = metrics['elbow']
            lines.append(f"Elbow Angle:")
            lines.append(f"  Average: {elbow['avg_angle']:.1f}° (optimal: 80-100°)")
            if elbow['left_avg'] and elbow['right_avg']:
                lines.append(f"  Left: {elbow['left_avg']:.1f}° | Right: {elbow['right_avg']:.1f}°")
            lines.append("")

        # Body rotation
        if metrics.get('rotation', {}).get('avg_rotation') is not None:
            rotation = metrics['rotation']
            lines.append(f"Body Rotation:")
            lines.append(f"  Average: {rotation['avg_rotation']:.1f}° (optimal: 45-60°)")
            lines.append(f"  Range: {rotation['min_rotation']:.1f}° - {rotation['max_rotation']:.1f}°")
            lines.append("")

        # Stroke rate
        if metrics.get('stroke_rate', {}).get('spm') is not None:
            sr = metrics['stroke_rate']
            lines.append(f"Stroke Rate:")
            lines.append(f"  {sr['spm']:.1f} strokes per minute (optimal: 50-60 SPM)")
            lines.append(f"  Duration: {sr['duration']:.1f}s | Total strokes: {sr['total_strokes']}")
            lines.append("")

        # Head stability
        if metrics.get('head', {}).get('stability') is not None:
            head = metrics['head']
            stability_pct = head['stability'] * 100
            lines.append(f"Head Stability: {stability_pct:.1f}% (higher is better)")
            lines.append("")

        # Kick
        if metrics.get('kick', {}).get('avg_knee_angle') is not None:
            kick = metrics['kick']
            lines.append(f"Kick Mechanics:")
            lines.append(f"  Knee angle: {kick['avg_knee_angle']:.1f}° (should be near 170°)")
            lines.append("")

        # Video quality
        if metrics.get('valid_frame_ratio') is not None:
            valid_pct = metrics['valid_frame_ratio'] * 100
            lines.append(f"Detection Quality: {valid_pct:.1f}% of frames analyzed")

        return "\n".join(lines)
