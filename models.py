"""Data models for student performance analysis."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Student:
    student_id: str
    name: str
    grades: dict[str, float] = field(default_factory=dict)

    @property
    def subject_count(self) -> int:
        return len(self.grades)

    def average(self) -> Optional[float]:
        if not self.grades:
            return None
        return sum(self.grades.values()) / len(self.grades)


@dataclass
class StudentReport:
    student_id: str
    name: str
    grades: dict[str, float]
    average: float
    letter_grade: str
    performance_level: str
    passed_subjects: int
    failed_subjects: int
    strongest_subject: str
    weakest_subject: str


@dataclass
class ClassSummary:
    total_students: int
    class_average: float
    highest_average: float
    lowest_average: float
    pass_rate: float
    subject_averages: dict[str, float]
    top_performers: list[str]
    at_risk_students: list[str]
