"""Streamlit web UI for the Student Performance Analyzer."""

import json
from dataclasses import asdict
from pathlib import Path

import streamlit as st

from analyzer import StudentPerformanceAnalyzer
from charts import (
    grade_distribution_chart,
    performance_breakdown_chart,
    student_rankings_chart,
    student_subject_chart,
    subject_averages_chart,
)
from data_loader import load_students, load_students_from_upload
from excel_export import export_analysis_to_bytes

SAMPLE_DATA = Path(__file__).parent / "sample_data.csv"


st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("Student Performance Analyzer")
st.caption("Upload grade data, explore insights, and export reports.")


@st.cache_data
def cached_load_students(filepath: str):
    return load_students(filepath)


def _analyzer_snapshot(analyzer: StudentPerformanceAnalyzer) -> dict:
    return {
        "summary": analyzer.class_summary(),
        "reports": analyzer.analyze_all(),
        "rankings": analyzer.rank_students(),
        "subject_stats": analyzer.subject_statistics(),
    }


def _render_metric_cards(summary) -> None:
    cols = st.columns(5)
    cols[0].metric("Students", summary.total_students)
    cols[1].metric("Class Average", f"{summary.class_average:.1f}")
    cols[2].metric("Pass Rate", f"{summary.pass_rate:.1f}%")
    cols[3].metric("Highest", f"{summary.highest_average:.1f}")
    cols[4].metric("Lowest", f"{summary.lowest_average:.1f}")


with st.sidebar:
    st.header("Settings")
    passing_grade = st.slider("Passing grade", min_value=0, max_value=100, value=60)
    data_source = st.radio("Data source", ["Sample data", "Upload file"])

    uploaded_file = None
    if data_source == "Upload file":
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx"],
            help="File must include student_id, name, and subject columns.",
        )

    st.divider()
    st.markdown("**Run from terminal:**")
    st.code("streamlit run app.py", language="bash")


try:
    if data_source == "Sample data":
        students = cached_load_students(str(SAMPLE_DATA))
    elif uploaded_file is not None:
        students = load_students_from_upload(uploaded_file, uploaded_file.name)
    else:
        st.info("Upload a CSV or Excel file to get started, or switch to **Sample data**.")
        st.stop()

    analyzer = StudentPerformanceAnalyzer(students, passing_grade=passing_grade)
    snapshot = _analyzer_snapshot(analyzer)
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.stop()

summary = snapshot["summary"]
reports = snapshot["reports"]
rankings = snapshot["rankings"]

_render_metric_cards(summary)

col_left, col_right = st.columns(2)
with col_left:
    if summary.top_performers:
        st.success(f"**Top performers:** {', '.join(summary.top_performers)}")
with col_right:
    if summary.at_risk_students:
        st.warning(f"**At-risk students:** {', '.join(summary.at_risk_students)}")
    else:
        st.success("No at-risk students.")

tab_overview, tab_rankings, tab_subjects, tab_student, tab_export = st.tabs(
    ["Overview", "Rankings", "Subjects", "Student Detail", "Export"]
)

with tab_overview:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.pyplot(subject_averages_chart(analyzer))
    with chart_col2:
        st.pyplot(performance_breakdown_chart(analyzer))
    st.pyplot(grade_distribution_chart(analyzer))

with tab_rankings:
    st.pyplot(student_rankings_chart(analyzer))
    ranking_data = [
        {
            "Rank": i,
            "Name": r.name,
            "ID": r.student_id,
            "Average": r.average,
            "Letter": r.letter_grade,
            "Level": r.performance_level,
        }
        for i, r in enumerate(rankings, start=1)
    ]
    st.dataframe(ranking_data, use_container_width=True, hide_index=True)

with tab_subjects:
    stats_rows = [
        {"Subject": subj, **stats}
        for subj, stats in snapshot["subject_stats"].items()
    ]
    st.dataframe(stats_rows, use_container_width=True, hide_index=True)

    subject_cols = st.columns(len(summary.subject_averages) or 1)
    for col, (subject, avg) in zip(subject_cols, summary.subject_averages.items()):
        col.metric(subject.title(), f"{avg:.1f}")

with tab_student:
    student_names = [r.name for r in rankings]
    selected_name = st.selectbox("Select a student", student_names)
    selected_report = next(r for r in reports if r.name == selected_name)

    detail_cols = st.columns(4)
    detail_cols[0].metric("Average", f"{selected_report.average:.1f}")
    detail_cols[1].metric("Letter Grade", selected_report.letter_grade)
    detail_cols[2].metric("Passed", selected_report.passed_subjects)
    detail_cols[3].metric("Failed", selected_report.failed_subjects)

    st.pyplot(student_subject_chart(selected_report, passing_grade=analyzer.passing_grade))

    grade_rows = [
        {"Subject": subj, "Score": score}
        for subj, score in sorted(selected_report.grades.items())
    ]
    st.dataframe(grade_rows, use_container_width=True, hide_index=True)

with tab_export:
    st.subheader("Download Reports")

    json_data = {
        "class_summary": asdict(summary),
        "student_reports": [asdict(r) for r in reports],
        "subject_statistics": snapshot["subject_stats"],
        "rankings": [{"rank": i, **asdict(r)} for i, r in enumerate(rankings, start=1)],
    }
    json_bytes = json.dumps(json_data, indent=2).encode("utf-8")
    excel_bytes = export_analysis_to_bytes(analyzer)

    dl_col1, dl_col2 = st.columns(2)
    dl_col1.download_button(
        label="Download JSON Report",
        data=json_bytes,
        file_name="student_performance_report.json",
        mime="application/json",
        use_container_width=True,
    )
    dl_col2.download_button(
        label="Download Excel Report",
        data=excel_bytes,
        file_name="student_performance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.caption("Excel export includes sheets for student reports, class summary, subject stats, and rankings.")
