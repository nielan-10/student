# Student Performance Analyzer

A Python tool for analyzing student grade data via CLI or an interactive web dashboard. Supports CSV and Excel import, visual charts, and JSON/Excel export.

## Features

- **CLI reports** — class summary, rankings, subject statistics, individual student reports
- **Web dashboard** — interactive Streamlit UI with charts and filters
- **Charts** — subject averages, rankings, grade distribution, performance breakdown
- **Excel support** — import `.xlsx` files and export multi-sheet workbooks
- **JSON export** — machine-readable full analysis output

## Requirements

- Python 3.10+
- See `requirements.txt` for dependencies

## Installation

```bash
cd student_performance_analyzer
pip install -r requirements.txt
```

## Quick Start

### Web UI (recommended)

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

### CLI

```bash
python main.py
```

## Data Format

Files must include `student_id`, `name`, and one column per subject (grades 0–100):

```csv
student_id,name,math,science,english,history,art
S001,Alice Johnson,92,88,95,90,87
S002,Bob Smith,65,70,58,62,72
```

Supported formats: **CSV** (`.csv`) and **Excel** (`.xlsx`).

## CLI Usage

```bash
# Full report with sample data
python main.py

# Your own CSV or Excel file
python main.py grades.csv
python main.py grades.xlsx

# Class summary only
python main.py --summary-only

# Student detail report
python main.py -s "Alice"

# Export reports
python main.py -e report.json
python main.py --excel-export report.xlsx

# Custom passing grade
python main.py --passing-grade 65
```

## Web Dashboard

The Streamlit app includes:

| Tab | Contents |
|-----|----------|
| **Overview** | Key metrics, subject averages, performance pie chart, grade histogram |
| **Rankings** | Horizontal bar chart and sortable table |
| **Subjects** | Per-subject mean, median, min, max, std dev |
| **Student Detail** | Individual grade chart and breakdown |
| **Export** | Download JSON or Excel reports |

Upload your own file from the sidebar, or use the built-in sample data.

## Excel Export Sheets

Exported `.xlsx` files contain:

1. **Student Reports** — all students with grades and analysis
2. **Class Summary** — aggregate metrics and subject averages
3. **Subject Statistics** — detailed per-subject stats
4. **Rankings** — ordered student list

## Grading Scale

| Average | Letter | Performance Level |
|---------|--------|-------------------|
| 90–100 | A | Excellent |
| 80–89 | B | Good |
| 70–79 | C | Average |
| 60–69 | D | Below Average |
| 0–59 | F | Needs Improvement |

## Project Structure

```
student_performance_analyzer/
├── app.py            # Streamlit web UI
├── main.py           # CLI entry point
├── analyzer.py       # Core analysis logic
├── charts.py         # Matplotlib visualizations
├── data_loader.py    # CSV/Excel loading
├── excel_export.py   # Excel report export
├── models.py         # Data classes
├── reporter.py       # CLI report formatting
├── sample_data.csv   # Example dataset
└── requirements.txt
```
