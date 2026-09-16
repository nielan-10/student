#!/usr/bin/env python3
"""Student Performance Analyzer - CLI entry point."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from analyzer import StudentPerformanceAnalyzer
from data_loader import load_students
from excel_export import export_analysis_to_file
from reporter import (
    format_class_summary,
    format_rankings,
    format_student_report,
    format_subject_stats,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze student academic performance from grade data.",
    )
    parser.add_argument(
        "data_file",
        nargs="?",
        default=str(Path(__file__).parent / "sample_data.csv"),
        help="Path to CSV file with student grades (default: sample_data.csv)",
    )
    parser.add_argument(
        "--student", "-s",
        metavar="NAME_OR_ID",
        help="Show detailed report for a specific student",
    )
    parser.add_argument(
        "--rankings", "-r",
        action="store_true",
        help="Show student rankings",
    )
    parser.add_argument(
        "--subjects",
        action="store_true",
        help="Show per-subject statistics",
    )
    parser.add_argument(
        "--passing-grade",
        type=float,
        default=60.0,
        help="Minimum passing grade (default: 60)",
    )
    parser.add_argument(
        "--export", "-e",
        metavar="FILE",
        help="Export full analysis report to JSON",
    )
    parser.add_argument(
        "--excel-export",
        metavar="FILE",
        help="Export full analysis report to Excel (.xlsx)",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only the class summary",
    )
    return parser


def export_json(analyzer: StudentPerformanceAnalyzer, filepath: Path) -> None:
    data = {
        "class_summary": asdict(analyzer.class_summary()),
        "student_reports": [asdict(r) for r in analyzer.analyze_all()],
        "subject_statistics": analyzer.subject_statistics(),
        "rankings": [
            {"rank": i, **asdict(r)}
            for i, r in enumerate(analyzer.rank_students(), start=1)
        ],
    }
    filepath.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        students = load_students(args.data_file)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    analyzer = StudentPerformanceAnalyzer(students, passing_grade=args.passing_grade)

    if args.student:
        student = analyzer.find_student(args.student)
        if not student:
            print(f"Error: No student found matching '{args.student}'", file=sys.stderr)
            return 1
        print(format_student_report(analyzer.analyze_student(student)))
        return 0

    print(format_class_summary(analyzer.class_summary()))

    if not args.summary_only:
        if args.rankings:
            print()
            print(format_rankings(analyzer))

        if args.subjects:
            print()
            print(format_subject_stats(analyzer))

        if not args.rankings and not args.subjects:
            print()
            print(format_rankings(analyzer))
            print()
            print(format_subject_stats(analyzer))

    if args.export:
        export_path = Path(args.export)
        export_json(analyzer, export_path)
        print(f"\nReport exported to {export_path}")

    if args.excel_export:
        excel_path = Path(args.excel_export)
        export_analysis_to_file(analyzer, str(excel_path))
        print(f"Excel report exported to {excel_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
