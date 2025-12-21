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

        # Overall rating
        rating = self._calculate_overall_rating(issues)

        # Group issues by severity
        critical_issues = [i for i in issues if i.severity == SEVERITY_CRITICAL]
        moderate_issues = [i for i in issues if i.severity == SEVERITY_MODERATE]
        minor_issues = [i for i in issues if i.severity == SEVERITY_MINOR]

        # ====== HEADER WITH SCORE ======
        report.append("🏊‍♂️ YOUR SWIM ANALYSIS")
        report.append("")
        report.append(f"Overall Technique Score: {rating}/10")
        report.append("")

        # ====== QUICK INSIGHT (THE HOOK) ======
        insight = self._generate_quick_insight(rating, critical_issues, moderate_issues)
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("📊 QUICK INSIGHT")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(insight)
        report.append("")

        # ====== BIGGEST RED FLAG (if any) ======
        if critical_issues:
            report.append("🚨 BIGGEST RED FLAG")
            report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            top_issue = critical_issues[0]
            report.append(f"⚠️  {top_issue.description}")
            report.append("")
            report.append(f"💡 HOW TO FIX IT:")
            report.append(f"   {top_issue.tip}")
            report.append("")
            if len(critical_issues) > 1:
                report.append(f"   (+ {len(critical_issues) - 1} more critical issue{'s' if len(critical_issues) > 2 else ''} detected)")
            report.append("")

        # ====== WHAT'S WORKING ======
        strengths = self._identify_strengths(metrics, issues)
        if strengths:
            report.append("✅ WHAT'S WORKING")
            report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for strength in strengths:
                report.append(f"• {strength}")
            report.append("")

        # ====== ACTION PLAN ======
        if critical_issues or moderate_issues:
            report.append("🎯 YOUR ACTION PLAN")
            report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            report.append("Focus on these in order:")
            report.append("")

            # Add critical issues
            for i, issue in enumerate(critical_issues, 1):
                report.append(f"{i}. 🚨 FIX THIS FIRST: {issue.description}")
                report.append(f"   → {issue.tip}")
                report.append("")

            # Add top moderate issues
            start_num = len(critical_issues) + 1
            for i, issue in enumerate(moderate_issues[:2], start_num):  # Only top 2 moderate
                report.append(f"{i}. ⚠️ IMPORTANT: {issue.description}")
                report.append(f"   → {issue.tip}")
                report.append("")

        # ====== DETAILED BREAKDOWN (Collapsed by default in UI) ======
        if critical_issues or moderate_issues or minor_issues:
            report.append("📋 DETAILED BREAKDOWN")
            report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            # Critical issues
            if critical_issues:
                report.append(f"{get_severity_emoji(SEVERITY_CRITICAL)} {get_severity_label(SEVERITY_CRITICAL)}:")
                for issue in critical_issues:
                    report.append(f"  • {issue.description}")
                    report.append(f"    → {issue.tip}")
                report.append("")

            # Moderate issues
            if moderate_issues:
                report.append(f"{get_severity_emoji(SEVERITY_MODERATE)} {get_severity_label(SEVERITY_MODERATE)}:")
                for issue in moderate_issues:
                    report.append(f"  • {issue.description}")
                    report.append(f"    → {issue.tip}")
                report.append("")

            # Minor issues
            if minor_issues:
                report.append(f"{get_severity_emoji(SEVERITY_MINOR)} {get_severity_label(SEVERITY_MINOR)}:")
                for issue in minor_issues:
                    report.append(f"  • {issue.description}")
                    report.append(f"    → {issue.tip}")
                report.append("")

        # ====== METRICS ======
        report.append("📊 YOUR NUMBERS")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append(self._format_metrics(metrics))
        report.append("")

        # ====== NO ISSUES CELEBRATION ======
        if not issues:
            report.append("🏆 EXCELLENT TECHNIQUE!")
            report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            report.append("No major technique issues detected! Your freestyle form is solid.")
            report.append("Keep up the great work and maintain that consistency!")
            report.append("")

        # ====== FOOTER WITH TIP ======
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("💡 PRO TIP: Focus on fixing one issue at a time.")
        report.append("   Trying to change everything at once = slower progress!")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

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

    def _generate_quick_insight(self, rating: int, critical_issues: List, moderate_issues: List) -> str:
        """Generate a quick, shareable insight about the swim."""
        if rating >= 9:
            return "🏆 Your technique is Olympic-level! Maintain this form and focus on consistency."
        elif rating >= 7:
            if critical_issues:
                return f"💪 Solid foundation, but you're losing speed/efficiency due to: {critical_issues[0].issue_type.replace('_', ' ')}. Fix that and you'll see big gains!"
            else:
                return "👍 Good technique overall! A few tweaks and you'll be swimming like a pro."
        elif rating >= 5:
            if critical_issues:
                return f"⚠️  Your biggest issue is: {critical_issues[0].issue_type.replace('_', ' ')}. This is costing you the most energy and speed. Focus here first!"
            else:
                return "🔧 Several areas need work, but they're all fixable! Follow the action plan below."
        else:
            if critical_issues:
                return f"🚨 Red flag alert: {critical_issues[0].issue_type.replace('_', ' ')}. This is significantly impacting your swim. Let's fix it step by step!"
            else:
                return "📚 You're just getting started! Follow the action plan and you'll see improvement quickly."

    def _identify_strengths(self, metrics: Dict, issues: List[FreestyleIssue]) -> List[str]:
        """Identify what the swimmer is doing well."""
        strengths = []

        # Check elbow angle
        if metrics.get('elbow', {}).get('avg_angle'):
            angle = metrics['elbow']['avg_angle']
            if 80 <= angle <= 100:
                strengths.append("Great elbow catch angle - you're engaging your lats properly!")

        # Check body rotation
        if metrics.get('rotation', {}).get('avg_rotation'):
            rotation = metrics['rotation']['avg_rotation']
            if 45 <= rotation <= 60:
                strengths.append("Excellent body rotation - you're using your core effectively!")

        # Check head stability
        if metrics.get('head', {}).get('stability'):
            stability = metrics['head']['stability']
            if stability > 0.8:
                strengths.append("Solid head position - you're maintaining good alignment!")

        # Check stroke rate
        if metrics.get('stroke_rate', {}).get('spm'):
            spm = metrics['stroke_rate']['spm']
            if 50 <= spm <= 60:
                strengths.append("Optimal stroke rate - nice rhythm and tempo!")

        # If no specific strengths but also few issues
        if not strengths and len(issues) <= 2:
            strengths.append("Your overall form is consistent across the video!")

        return strengths

    def _format_metrics(self, metrics: Dict) -> str:
        """Format metrics section."""
        lines = []

        # Elbow metrics
        if metrics.get('elbow', {}).get('avg_angle') is not None:
            elbow = metrics['elbow']
            lines.append(f"🔸 Elbow Catch Angle:")
            lines.append(f"   Average: {elbow['avg_angle']:.1f}° (optimal: 80-100°)")
            if elbow['left_avg'] and elbow['right_avg']:
                lines.append(f"   Left: {elbow['left_avg']:.1f}° | Right: {elbow['right_avg']:.1f}°")
            lines.append("")

        # Body rotation
        if metrics.get('rotation', {}).get('avg_rotation') is not None:
            rotation = metrics['rotation']
            lines.append(f"🔸 Body Rotation:")
            lines.append(f"   Average: {rotation['avg_rotation']:.1f}° (optimal: 45-60°)")
            lines.append(f"   Range: {rotation['min_rotation']:.1f}° - {rotation['max_rotation']:.1f}°")
            lines.append("")

        # Stroke rate
        if metrics.get('stroke_rate', {}).get('spm') is not None:
            sr = metrics['stroke_rate']
            lines.append(f"🔸 Stroke Rate:")
            lines.append(f"   {sr['spm']:.1f} strokes per minute (optimal: 50-60 SPM)")
            lines.append(f"   Duration: {sr['duration']:.1f}s | Total strokes: {sr['total_strokes']}")
            lines.append("")

        # Head stability
        if metrics.get('head', {}).get('stability') is not None:
            head = metrics['head']
            stability_pct = head['stability'] * 100
            lines.append(f"🔸 Head Stability: {stability_pct:.1f}% (higher is better)")
            lines.append("")

        # Kick
        if metrics.get('kick', {}).get('avg_knee_angle') is not None:
            kick = metrics['kick']
            lines.append(f"🔸 Kick Mechanics:")
            lines.append(f"   Knee angle: {kick['avg_knee_angle']:.1f}° (should be near 170°)")
            lines.append("")

        # Video quality
        if metrics.get('valid_frame_ratio') is not None:
            valid_pct = metrics['valid_frame_ratio'] * 100
            lines.append(f"🔸 Detection Quality: {valid_pct:.1f}% of frames analyzed")

        return "\n".join(lines)
