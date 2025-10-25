from django.core.management.base import BaseCommand
from cms_plugins.models import Student, Course, Enrollment, Grade, Attendance
from django.utils import timezone
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for the Student Dashboard Plugin'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample courses
        courses_data = [
            {
                'title': 'Introduction to Computer Science',
                'code': 'CS101',
                'description': 'Fundamental concepts of computer science and programming.',
                'category': 'technology',
                'instructor': 'Dr. Smith',
                'credits': 3,
                'duration': '15 weeks'
            },
            {
                'title': 'Calculus I',
                'code': 'MATH101',
                'description': 'Introduction to differential and integral calculus.',
                'category': 'science',
                'instructor': 'Prof. Johnson',
                'credits': 4,
                'duration': '15 weeks'
            },
            {
                'title': 'English Composition',
                'code': 'ENG101',
                'description': 'Development of writing skills and critical thinking.',
                'category': 'arts',
                'instructor': 'Dr. Williams',
                'credits': 3,
                'duration': '15 weeks'
            },
            {
                'title': 'Introduction to Psychology',
                'code': 'PSY101',
                'description': 'Survey of major concepts and theories in psychology.',
                'category': 'science',
                'instructor': 'Dr. Brown',
                'credits': 3,
                'duration': '15 weeks'
            }
        ]
        
        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults=course_data
            )
            courses.append(course)
            if created:
                self.stdout.write(f"Created course: {course}")
            else:
                self.stdout.write(f"Course already exists: {course}")
        
        # Create sample students
        students_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'student_id': 'STU123456',
                'email': 'john.doe@example.com',
                'date_of_birth': date(2000, 5, 15),
                'enrollment_date': date(2022, 9, 1)
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'student_id': 'STU654321',
                'email': 'jane.smith@example.com',
                'date_of_birth': date(1999, 12, 3),
                'enrollment_date': date(2021, 9, 1)
            }
        ]
        
        students = []
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                student_id=student_data['student_id'],
                defaults=student_data
            )
            students.append(student)
            if created:
                self.stdout.write(f"Created student: {student}")
            else:
                self.stdout.write(f"Student already exists: {student}")
        
        # Create enrollments
        for student in students:
            for course in courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'enrollment_date': date(2023, 9, 1),
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f"Created enrollment: {student} in {course}")
                else:
                    self.stdout.write(f"Enrollment already exists: {student} in {course}")
        
        # Create grades
        grades_data = [
            {
                'student': students[0],
                'course': courses[0],
                'grade': 'A-',
                'semester': 'Fall 2023'
            },
            {
                'student': students[0],
                'course': courses[1],
                'grade': 'B+',
                'semester': 'Fall 2023'
            },
            {
                'student': students[0],
                'course': courses[2],
                'grade': 'A',
                'semester': 'Fall 2023'
            },
            {
                'student': students[1],
                'course': courses[0],
                'grade': 'B',
                'semester': 'Fall 2023'
            },
            {
                'student': students[1],
                'course': courses[3],
                'grade': 'A+',
                'semester': 'Fall 2023'
            }
        ]
        
        for grade_data in grades_data:
            grade, created = Grade.objects.get_or_create(
                student=grade_data['student'],
                course=grade_data['course'],
                defaults={
                    'grade': grade_data['grade'],
                    'semester': grade_data['semester']
                }
            )
            if created:
                self.stdout.write(f"Created grade: {grade_data['student']} - {grade_data['course']}: {grade_data['grade']}")
            else:
                self.stdout.write(f"Grade already exists: {grade_data['student']} - {grade_data['course']}: {grade.grade}")
        
        # Create attendance records
        # Generate attendance for the last 30 days
        today = date.today()
        for i in range(30):
            attendance_date = today - timedelta(days=i)
            
            for student in students:
                for course in courses:
                    # Randomly decide if student was present (80% chance)
                    is_present = random.random() < 0.8
                    
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=attendance_date,
                        defaults={
                            'is_present': is_present,
                            'is_excused': False
                        }
                    )
                    if created:
                        status = "Present" if is_present else "Absent"
                        self.stdout.write(f"Created attendance: {student} - {course} on {attendance_date}: {status}")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )