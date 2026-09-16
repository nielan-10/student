"""Core student performance analysis logic."""

from statistics import mean, median, stdev

from models import ClassSummary, Student, StudentReport


PASSING_GRADE = 60.0
EXCELLENT_THRESHOLD = 90.0
GOOD_THRESHOLD = 80.0
AVERAGE_THRESHOLD = 70.0


def letter_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def performance_level(score: float) -> str:
    if score >= EXCELLENT_THRESHOLD:
        return "Excellent"
    if score >= GOOD_THRESHOLD:
        return "Good"
    if score >= AVERAGE_THRESHOLD:
        return "Average"
    if score >= PASSING_GRADE:
        return "Below Average"
    return "Needs Improvement"


class StudentPerformanceAnalyzer:
    def __init__(self, students: list[Student], passing_grade: float = PASSING_GRADE):
        self.students = students
        self.passing_grade = passing_grade

    def analyze_student(self, student: Student) -> StudentReport:
        if not student.grades:
            raise ValueError(f"Student {student.name} has no grades")

        avg = student.average()
        assert avg is not None

        passed = sum(1 for g in student.grades.values() if g >= self.passing_grade)
        failed = len(student.grades) - passed

        strongest = max(student.grades, key=student.grades.get)
        weakest = min(student.grades, key=student.grades.get)

        return StudentReport(
            student_id=student.student_id,
            name=student.name,
            grades=dict(student.grades),
            average=round(avg, 2),
            letter_grade=letter_grade(avg),
            performance_level=performance_level(avg),
            passed_subjects=passed,
            failed_subjects=failed,
            strongest_subject=strongest,
            weakest_subject=weakest,
        )

    def analyze_all(self) -> list[StudentReport]:
        return [self.analyze_student(s) for s in self.students]

    def class_summary(self) -> ClassSummary:
        reports = self.analyze_all()
        averages = [r.average for r in reports]

        all_grades = [g for s in self.students for g in s.grades.values()]
        pass_rate = (
            sum(1 for g in all_grades if g >= self.passing_grade) / len(all_grades) * 100
            if all_grades
            else 0.0
        )

        subjects: set[str] = set()
        for s in self.students:
            subjects.update(s.grades.keys())

        subject_averages = {}
        for subject in sorted(subjects):
            scores = [s.grades[subject] for s in self.students if subject in s.grades]
            subject_averages[subject] = round(mean(scores), 2)

        sorted_reports = sorted(reports, key=lambda r: r.average, reverse=True)
        top_count = max(1, len(reports) // 5)
        top_performers = [r.name for r in sorted_reports[:top_count]]
        at_risk = [r.name for r in reports if r.average < self.passing_grade]

        return ClassSummary(
            total_students=len(reports),
            class_average=round(mean(averages), 2),
            highest_average=max(averages),
            lowest_average=min(averages),
            pass_rate=round(pass_rate, 2),
            subject_averages=subject_averages,
            top_performers=top_performers,
            at_risk_students=at_risk,
        )

    def subject_statistics(self) -> dict[str, dict[str, float]]:
        subjects: set[str] = set()
        for s in self.students:
            subjects.update(s.grades.keys())

        stats = {}
        for subject in sorted(subjects):
            scores = [s.grades[subject] for s in self.students if subject in s.grades]
            entry: dict[str, float] = {
                "mean": round(mean(scores), 2),
                "median": round(median(scores), 2),
                "min": min(scores),
                "max": max(scores),
            }
            if len(scores) > 1:
                entry["std_dev"] = round(stdev(scores), 2)
            else:
                entry["std_dev"] = 0.0
            stats[subject] = entry

        return stats

    def find_student(self, query: str) -> Student | None:
        query_lower = query.lower()
        for student in self.students:
            if (
                student.student_id.lower() == query_lower
                or student.name.lower() == query_lower
                or query_lower in student.name.lower()
            ):
                return student
        return None

    def rank_students(self) -> list[StudentReport]:
        return sorted(self.analyze_all(), key=lambda r: r.average, reverse=True)
