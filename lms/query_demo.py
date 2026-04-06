from django.db import connection, reset_queries
from lms.models import Course, Enrollment

print("=" * 50)
print("N+1 QUERY DEMO")
print("=" * 50)

reset_queries()
courses = Course.objects.all()

for course in courses[:2]:   # cuma tampilkan 2 contoh
    print(f"Course: {course.title}")
    print(f"Instructor: {course.instructor.username}")
    print(f"Category: {course.category.name}")
    print(f"Lessons: {course.lessons.count()}")
    print("-" * 30)

print(f"Total Queries (N+1 version): {len(connection.queries)}")


print("\n" + "=" * 50)
print("OPTIMIZED QUERY DEMO")
print("=" * 50)

reset_queries()
courses = Course.objects.for_listing()

for course in courses[:2]:   # cuma tampilkan 2 contoh
    print(f"Course: {course.title}")
    print(f"Instructor: {course.instructor.username}")
    print(f"Category: {course.category.name}")
    print(f"Lessons: {course.lesson_count}")
    print(f"Students: {course.student_count}")
    print("-" * 30)

print(f"Total Queries (Optimized version): {len(connection.queries)}")


print("\n" + "=" * 50)
print("ENROLLMENT DASHBOARD DEMO")
print("=" * 50)

reset_queries()
enrollments = Enrollment.objects.for_student_dashboard()

for enrollment in enrollments[:3]:   # cuma tampilkan 3 contoh
    print(f"Student: {enrollment.student.username}")
    print(f"Course: {enrollment.course.title}")
    print(f"Category: {enrollment.course.category.name}")
    print(f"Instructor: {enrollment.course.instructor.username}")
    print(f"Lessons: {enrollment.course.lessons.count()}")
    print(f"Progress Records: {enrollment.progress_records.count()}")
    print("-" * 30)

print(f"Total Queries (Dashboard optimized): {len(connection.queries)}")