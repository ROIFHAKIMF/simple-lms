from typing import Optional
from ninja import Router, Query
from ninja.errors import HttpError
from django.http import HttpRequest

from ..models import Course, Category
from ..permissions import jwt_auth, is_instructor, is_admin
from ..schemas import (
    CourseListOut, CourseDetailOut,
    CourseIn, CoursePatchIn,
    PaginatedCourses, MessageOut,
)

router = Router(tags=["Courses"])


def _course_list_out(course) -> CourseListOut:
    cat = None
    if course.category:
        from ..schemas import CategoryOut
        cat = CategoryOut(
            id=course.category.id,
            name=course.category.name,
            parent_id=course.category.parent_id,
        )
    return CourseListOut(
        id=course.id,
        title=course.title,
        description=course.description,
        instructor_id=course.instructor_id,
        instructor_name=course.instructor.get_full_name() or course.instructor.username,
        category=cat,
        lesson_count=getattr(course, "lesson_count", course.lessons.count()),
        student_count=getattr(course, "student_count", course.enrollments.count()),
        created_at=course.created_at,
    )


def _course_detail_out(course) -> CourseDetailOut:
    cat = None
    if course.category:
        from ..schemas import CategoryOut
        cat = CategoryOut(
            id=course.category.id,
            name=course.category.name,
            parent_id=course.category.parent_id,
        )
    return CourseDetailOut(
        id=course.id,
        title=course.title,
        description=course.description,
        instructor_id=course.instructor_id,
        instructor_name=course.instructor.get_full_name() or course.instructor.username,
        category=cat,
        created_at=course.created_at,
    )


# ─────────────────────────────────────────
# PUBLIC ENDPOINTS
# ─────────────────────────────────────────

@router.get("", response=PaginatedCourses, summary="List all courses (public)")
def list_courses(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
):
    """
    Returns a paginated list of all courses.
    Optionally filter by **search** (title/description) or **category_id**.
    """
    qs = Course.objects.for_listing()

    if search:
        qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)
        # Re-apply optimization after OR
        qs = Course.objects.for_listing().filter(
            title__icontains=search
        ) | Course.objects.for_listing().filter(description__icontains=search)
        # Simpler approach
        qs = Course.objects.for_listing().filter(
            title__icontains=search
        )
    if category_id:
        qs = Course.objects.for_listing().filter(category_id=category_id)
    if search and category_id:
        qs = Course.objects.for_listing().filter(
            title__icontains=search, category_id=category_id
        )
    if not search and not category_id:
        qs = Course.objects.for_listing()

    total = qs.count()
    offset = (page - 1) * page_size
    courses = qs[offset: offset + page_size]

    return PaginatedCourses(
        total=total,
        page=page,
        page_size=page_size,
        results=[_course_list_out(c) for c in courses],
    )


@router.get("/{course_id}", response=CourseDetailOut, summary="Course detail (public)")
def get_course(request: HttpRequest, course_id: int):
    """Return details for a single course."""
    try:
        course = Course.objects.select_related("instructor", "category").get(pk=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")
    return _course_detail_out(course)


# ─────────────────────────────────────────
# PROTECTED ENDPOINTS
# ─────────────────────────────────────────

@router.post("", response=CourseDetailOut, auth=jwt_auth, summary="Create course (Instructor)")
@is_instructor
def create_course(request: HttpRequest, data: CourseIn):
    """Create a new course. Requires **instructor** or **admin** role."""
    category = None
    if data.category_id:
        try:
            category = Category.objects.get(pk=data.category_id)
        except Category.DoesNotExist:
            raise HttpError(404, "Category not found")

    course = Course.objects.create(
        title=data.title,
        description=data.description,
        instructor=request.user,
        category=category,
    )
    course = Course.objects.select_related("instructor", "category").get(pk=course.pk)
    return _course_detail_out(course)


@router.patch("/{course_id}", response=CourseDetailOut, auth=jwt_auth, summary="Update course (Owner)")
def update_course(request: HttpRequest, course_id: int, data: CoursePatchIn):
    """Update a course. Only the **owner** (or admin) can update."""
    try:
        course = Course.objects.select_related("instructor", "category").get(pk=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")

    user = request.user
    role = getattr(getattr(user, "profile", None), "role", "student")

    if course.instructor_id != user.id and role != "admin":
        raise HttpError(403, "You are not the owner of this course")

    if data.title is not None:
        course.title = data.title
    if data.description is not None:
        course.description = data.description
    if data.category_id is not None:
        try:
            course.category = Category.objects.get(pk=data.category_id)
        except Category.DoesNotExist:
            raise HttpError(404, "Category not found")

    course.save()
    course.refresh_from_db()
    return _course_detail_out(course)


@router.delete("/{course_id}", response=MessageOut, auth=jwt_auth, summary="Delete course (Admin)")
@is_admin
def delete_course(request: HttpRequest, course_id: int):
    """Delete a course. Requires **admin** role."""
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")
    course.delete()
    return MessageOut(message=f"Course '{course.title}' deleted successfully")