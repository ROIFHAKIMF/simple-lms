from ninja import Router
from ninja.errors import HttpError
from django.http import HttpRequest
from django.utils import timezone
from django.db import IntegrityError

from ..models import Course, Enrollment, Lesson, Progress
from ..permissions import jwt_auth, is_student
from ..schemas import (
    EnrollIn, EnrollmentOut, EnrollmentDetailOut,
    ProgressIn, ProgressOut, LessonOut, MessageOut,
)

router = Router(tags=["Enrollments"])


def _progress_out(p: Progress) -> ProgressOut:
    return ProgressOut(
        lesson_id=p.lesson_id,
        lesson_title=p.lesson.title,
        completed=p.completed,
        completed_at=p.completed_at,
    )


def _enrollment_detail_out(enrollment: Enrollment) -> EnrollmentDetailOut:
    lessons = [
        LessonOut(id=l.id, title=l.title, content=l.content, order=l.order)
        for l in enrollment.course.lessons.all()
    ]
    progress = [_progress_out(p) for p in enrollment.progress_records.select_related("lesson").all()]
    return EnrollmentDetailOut(
        id=enrollment.id,
        course_id=enrollment.course_id,
        course_title=enrollment.course.title,
        instructor_name=(
            enrollment.course.instructor.get_full_name()
            or enrollment.course.instructor.username
        ),
        enrolled_at=enrollment.enrolled_at,
        lessons=lessons,
        progress=progress,
    )


@router.post("", response=EnrollmentOut, auth=jwt_auth, summary="Enroll in a course (Student)")
@is_student
def enroll(request: HttpRequest, data: EnrollIn):
    """Enroll the authenticated student in a course."""
    try:
        course = Course.objects.get(pk=data.course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")

    try:
        enrollment = Enrollment.objects.create(student=request.user, course=course)
    except IntegrityError:
        raise HttpError(400, "Already enrolled in this course")

    return EnrollmentOut(
        id=enrollment.id,
        course_id=enrollment.course_id,
        course_title=course.title,
        enrolled_at=enrollment.enrolled_at,
    )


@router.get(
    "/my-courses",
    response=list[EnrollmentDetailOut],
    auth=jwt_auth,
    summary="Get my enrolled courses",
)
def my_courses(request: HttpRequest):
    """Return all courses the authenticated user is enrolled in, with progress."""
    enrollments = (
        Enrollment.objects.for_student_dashboard().filter(student=request.user)
    )
    return [_enrollment_detail_out(e) for e in enrollments]


@router.post(
    "/{enrollment_id}/progress",
    response=ProgressOut,
    auth=jwt_auth,
    summary="Mark lesson complete / incomplete",
)
def mark_progress(request: HttpRequest, enrollment_id: int, data: ProgressIn):
    """
    Mark a lesson as complete (or incomplete).
    The authenticated user must own this enrollment.
    """
    try:
        enrollment = Enrollment.objects.select_related(
            "course", "student"
        ).get(pk=enrollment_id)
    except Enrollment.DoesNotExist:
        raise HttpError(404, "Enrollment not found")

    if enrollment.student_id != request.user.id:
        raise HttpError(403, "This enrollment does not belong to you")

    try:
        lesson = Lesson.objects.get(pk=data.lesson_id, course=enrollment.course)
    except Lesson.DoesNotExist:
        raise HttpError(404, "Lesson not found in this course")

    progress, _ = Progress.objects.get_or_create(
        enrollment=enrollment, lesson=lesson
    )
    progress.completed = data.completed
    progress.completed_at = timezone.now() if data.completed else None
    progress.save()

    return ProgressOut(
        lesson_id=lesson.id,
        lesson_title=lesson.title,
        completed=progress.completed,
        completed_at=progress.completed_at,
    )