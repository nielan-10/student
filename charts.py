"""Matplotlib charts for student performance visualization."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from analyzer import StudentPerformanceAnalyzer
from models import StudentReport

LEVEL_COLORS = {
    "Excellent": "#2ecc71",
    "Good": "#3498db",
    "Average": "#f1c40f",
    "Below Average": "#e67e22",
    "Needs Improvement": "#e74c3c",
}


def _apply_style(fig: Figure) -> None:
    fig.patch.set_facecolor("#fafafa")
    for ax in fig.axes:
        ax.set_facecolor("#ffffff")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.3, linestyle="--")


def subject_averages_chart(analyzer: StudentPerformanceAnalyzer) -> Figure:
    summary = analyzer.class_summary()
    subjects = list(summary.subject_averages.keys())
    averages = list(summary.subject_averages.values())

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(subjects, averages, color="#3498db", edgecolor="white")
    ax.axhline(y=analyzer.passing_grade, color="#e74c3c", linestyle="--",
               linewidth=1.5, label=f"Passing ({analyzer.passing_grade})")
    ax.set_ylabel("Average Score")
    ax.set_title("Subject Averages")
    ax.set_ylim(0, 100)
    ax.legend()

    for bar, avg in zip(bars, averages):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{avg:.1f}", ha="center", va="bottom", fontsize=9)

    plt.xticks(rotation=30, ha="right")
    _apply_style(fig)
    fig.tight_layout()
    return fig


def student_rankings_chart(analyzer: StudentPerformanceAnalyzer) -> Figure:
    reports = analyzer.rank_students()
    names = [r.name for r in reports]
    averages = [r.average for r in reports]
    colors = [LEVEL_COLORS.get(r.performance_level, "#95a5a6") for r in reports]

    fig, ax = plt.subplots(figsize=(8, max(4, len(names) * 0.4)))
    bars = ax.barh(names, averages, color=colors, edgecolor="white")
    ax.axvline(x=analyzer.passing_grade, color="#e74c3c", linestyle="--",
               linewidth=1.5, label=f"Passing ({analyzer.passing_grade})")
    ax.set_xlabel("Average Score")
    ax.set_title("Student Rankings")
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.legend()

    for bar, avg in zip(bars, averages):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{avg:.1f}", ha="left", va="center", fontsize=9)

    _apply_style(fig)
    fig.tight_layout()
    return fig


def grade_distribution_chart(analyzer: StudentPerformanceAnalyzer) -> Figure:
    all_grades = [g for s in analyzer.students for g in s.grades.values()]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(all_grades, bins=10, range=(0, 100), color="#9b59b6",
            edgecolor="white", alpha=0.85)
    ax.axvline(x=analyzer.passing_grade, color="#e74c3c", linestyle="--",
               linewidth=1.5, label=f"Passing ({analyzer.passing_grade})")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Count")
    ax.set_title("Grade Distribution")
    ax.legend()

    _apply_style(fig)
    fig.tight_layout()
    return fig


def performance_breakdown_chart(analyzer: StudentPerformanceAnalyzer) -> Figure:
    reports = analyzer.analyze_all()
    level_counts: dict[str, int] = {}
    for report in reports:
        level_counts[report.performance_level] = level_counts.get(report.performance_level, 0) + 1

    order = ["Excellent", "Good", "Average", "Below Average", "Needs Improvement"]
    labels = [lvl for lvl in order if lvl in level_counts]
    counts = [level_counts[lvl] for lvl in labels]
    colors = [LEVEL_COLORS[lvl] for lvl in labels]

    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        counts, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, textprops={"fontsize": 9},
    )
    ax.set_title("Performance Level Breakdown")
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    _apply_style(fig)
    fig.tight_layout()
    return fig


def student_subject_chart(report: StudentReport, passing_grade: float = 60.0) -> Figure:
    subjects = list(report.grades.keys())
    scores = list(report.grades.values())

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(subjects, scores, color="#1abc9c", edgecolor="white")
    ax.axhline(y=passing_grade, color="#e74c3c", linestyle="--", linewidth=1.5,
               label=f"Passing ({passing_grade})")
    ax.set_ylabel("Score")
    ax.set_title(f"{report.name} — Subject Grades (Avg: {report.average:.1f})")
    ax.set_ylim(0, 100)
    ax.legend()

    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{score:.0f}", ha="center", va="bottom", fontsize=9)

    plt.xticks(rotation=30, ha="right")
    _apply_style(fig)
    fig.tight_layout()
    return fig
