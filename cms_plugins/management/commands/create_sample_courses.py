from django.core.management.base import BaseCommand
from cms_plugins.models import Course

class Command(BaseCommand):
    help = 'Create sample courses for testing'

    def handle(self, *args, **options):
        # Create sample courses
        courses_data = [
            {
                'code': 'CS101',
                'title': 'Introduction to Computer Science',
                'description': 'An introductory course covering the fundamentals of computer science, programming, and computational thinking. Topics include algorithms, data structures, and software development principles.',
                'category': 'technology',
                'instructor': 'Dr. Jane Smith',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'MATH201',
                'title': 'Calculus II',
                'description': 'A continuation of Calculus I, covering techniques of integration, applications of integrals, sequences and series, and an introduction to differential equations.',
                'category': 'science',
                'instructor': 'Prof. John Doe',
                'credits': 4,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'ENG102',
                'title': 'English Composition',
                'description': 'Development of writing skills through practice in various forms of prose, with emphasis on critical thinking, research, and argumentation.',
                'category': 'arts',
                'instructor': 'Dr. Emily Johnson',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'BUS150',
                'title': 'Introduction to Business',
                'description': 'Survey of the business world including management, marketing, finance, and operations. Designed to provide students with a broad understanding of business principles and practices.',
                'category': 'business',
                'instructor': 'Prof. Michael Brown',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'PHYS201',
                'title': 'General Physics I',
                'description': 'First course in a two-semester sequence covering mechanics, heat, and sound. Includes laboratory work and problem solving.',
                'category': 'science',
                'instructor': 'Dr. Robert Wilson',
                'credits': 4,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'CS301',
                'title': 'Data Structures and Algorithms',
                'description': 'Advanced study of data structures and algorithms, including trees, graphs, sorting, searching, and complexity analysis. Implementation in a high-level programming language.',
                'category': 'technology',
                'instructor': 'Dr. Jane Smith',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'ART110',
                'title': 'Introduction to Art History',
                'description': 'Survey of major periods and movements in Western art from ancient times to the present, with emphasis on visual analysis and cultural context.',
                'category': 'arts',
                'instructor': 'Prof. Sarah Davis',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            },
            {
                'code': 'ECON101',
                'title': 'Principles of Economics',
                'description': 'Introduction to economic principles and their application to current problems. Topics include supply and demand, market structures, national income, and monetary policy.',
                'category': 'business',
                'instructor': 'Dr. William Taylor',
                'credits': 3,
                'duration': '15 weeks',
                'is_published': True
            }
        ]

        for data in courses_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'category': data['category'],
                    'instructor': data['instructor'],
                    'credits': data['credits'],
                    'duration': data['duration'],
                    'is_published': data['is_published']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created course: {course.title} ({course.code})')
                )
            else:
                self.stdout.write(
                    f'Course already exists: {course.title} ({course.code})'
                )