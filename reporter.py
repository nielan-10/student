"""Format and display analysis reports."""

from analyzer import StudentPerformanceAnalyzer
from models import ClassSummary, StudentReport


def _bar(value: float, width: int = 20) -> str:
    filled = int(round(value / 100 * width))
    return "#" * filled + "-" * (width - filled)


def format_student_report(report: StudentReport) -> str:
    lines = [
        f"Student: {report.name} ({report.student_id})",
        f"  Average: {report.average:.1f}  |  Letter: {report.letter_grade}  |  Level: {report.performance_level}",
        f"  Passed: {report.passed_subjects}  |  Failed: {report.failed_subjects}",
        f"  Strongest: {report.strongest_subject}  |  Weakest: {report.weakest_subject}",
        "  Grades:",
    ]
    for subject, grade in sorted(report.grades.items()):
        lines.append(f"    {subject:12s} {grade:5.1f}  {_bar(grade)}")
    return "\n".join(lines)


def format_class_summary(summary: ClassSummary) -> str:
    lines = [
        "=== Class Summary ===",
        f"Total Students:    {summary.total_students}",
        f"Class Average:     {summary.class_average:.1f}",
        f"Highest Average:   {summary.highest_average:.1f}",
        f"Lowest Average:    {summary.lowest_average:.1f}",
        f"Pass Rate:         {summary.pass_rate:.1f}%",
        "",
        "Subject Averages:",
    ]
    for subject, avg in summary.subject_averages.items():
        lines.append(f"  {subject:12s} {avg:5.1f}  {_bar(avg)}")
    lines.extend(
        [
            "",
            f"Top Performers:    {', '.join(summary.top_performers) or 'None'}",
            f"At-Risk Students:  {', '.join(summary.at_risk_students) or 'None'}",
        ]
    )
    return "\n".join(lines)


def format_rankings(analyzer: StudentPerformanceAnalyzer) -> str:
    lines = ["=== Student Rankings ===", f"{'Rank':<6}{'Name':<20}{'Avg':>8}{'Grade':>8}{'Level':>18}"]
    lines.append("-" * 60)
    for rank, report in enumerate(analyzer.rank_students(), start=1):
        lines.append(
            f"{rank:<6}{report.name:<20}{report.average:>8.1f}"
            f"{report.letter_grade:>8}{report.performance_level:>18}"
        )
    return "\n".join(lines)


def format_subject_stats(analyzer: StudentPerformanceAnalyzer) -> str:
    stats = analyzer.subject_statistics()
    lines = [
        "=== Subject Statistics ===",
        f"{'Subject':<12}{'Mean':>8}{'Median':>8}{'Min':>8}{'Max':>8}{'Std Dev':>10}",
    ]
    lines.append("-" * 54)
    for subject, data in stats.items():
        lines.append(
            f"{subject:<12}{data['mean']:>8.1f}{data['median']:>8.1f}"
            f"{data['min']:>8.1f}{data['max']:>8.1f}{data['std_dev']:>10.2f}"
        )
    return "\n".join(lines)
