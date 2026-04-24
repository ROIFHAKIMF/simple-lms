from typing import Optional, List
from datetime import datetime
from ninja import Schema


# ─────────────────────────────────────────
# AUTH SCHEMAS
# ─────────────────────────────────────────

class RegisterIn(Schema):
    username: str
    email: str
    password: str
    role: str = "student"  # admin | instructor | student


class LoginIn(Schema):
    username: str
    password: str


class RefreshIn(Schema):
    refresh_token: str


class TokenOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenOut(Schema):
    access_token: str
    token_type: str = "bearer"


class ProfileOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str


class ProfileUpdateIn(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


# ─────────────────────────────────────────
# CATEGORY SCHEMAS
# ─────────────────────────────────────────

class CategoryOut(Schema):
    id: int
    name: str
    parent_id: Optional[int] = None


# ─────────────────────────────────────────
# COURSE SCHEMAS
# ─────────────────────────────────────────

class CourseListOut(Schema):
    id: int
    title: str
    description: str
    instructor_id: int
    instructor_name: str
    category: Optional[CategoryOut] = None
    lesson_count: int
    student_count: int
    created_at: datetime


class CourseDetailOut(Schema):
    id: int
    title: str
    description: str
    instructor_id: int
    instructor_name: str
    category: Optional[CategoryOut] = None
    created_at: datetime


class CourseIn(Schema):
    title: str
    description: str
    category_id: Optional[int] = None


class CoursePatchIn(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class PaginatedCourses(Schema):
    total: int
    page: int
    page_size: int
    results: List[CourseListOut]


# ─────────────────────────────────────────
# LESSON SCHEMAS
# ─────────────────────────────────────────

class LessonOut(Schema):
    id: int
    title: str
    content: str
    order: int


# ─────────────────────────────────────────
# ENROLLMENT SCHEMAS
# ─────────────────────────────────────────

class EnrollIn(Schema):
    course_id: int


class EnrollmentOut(Schema):
    id: int
    course_id: int
    course_title: str
    enrolled_at: datetime


class ProgressIn(Schema):
    lesson_id: int
    completed: bool = True


class ProgressOut(Schema):
    lesson_id: int
    lesson_title: str
    completed: bool
    completed_at: Optional[datetime] = None


class EnrollmentDetailOut(Schema):
    id: int
    course_id: int
    course_title: str
    instructor_name: str
    enrolled_at: datetime
    lessons: List[LessonOut]
    progress: List[ProgressOut]


# ─────────────────────────────────────────
# GENERIC
# ─────────────────────────────────────────

class MessageOut(Schema):
    message: str