from django.core.management.base import BaseCommand
from cms_plugins.models import Announcement

class Command(BaseCommand):
    help = 'Create sample announcements with long content for testing Read More functionality'

    def handle(self, *args, **options):
        # Create sample announcements with long content
        announcements_data = [
            {
                'title': 'University Wide System Maintenance',
                'content': '''The university IT department will be performing system maintenance across all campus networks this weekend. This maintenance will affect access to student portals, online learning platforms, and email services.

During the maintenance window (Saturday 12:00 AM to Sunday 6:00 AM), the following services will be temporarily unavailable:
- Student Information System (SIS)
- Learning Management System (LMS)
- University email services
- Online library resources
- Campus WiFi networks

We recommend that students and faculty complete any critical work before the maintenance begins. For urgent matters during the maintenance period, please contact the IT Help Desk at helpdesk@university.edu or call (555) 123-4567.

The maintenance is necessary to upgrade our core infrastructure and improve system performance and security. We apologize for any inconvenience this may cause and appreciate your patience as we work to enhance our services.

Additional information and updates will be posted on the university website and social media channels. Thank you for your understanding and cooperation.

If you have any questions or concerns, please don't hesitate to reach out to the IT department. We value your feedback and are committed to providing the best possible service to our university community.

This maintenance is part of our ongoing commitment to maintaining a secure and efficient technology environment for all students, faculty, and staff members.''',
                'is_published': True
            },
            {
                'title': 'New Academic Policies for Spring Semester',
                'content': '''Beginning with the Spring semester, the university will implement several new academic policies designed to enhance the educational experience and ensure academic integrity.

Key changes include:
1. Updated attendance policy requiring 90% attendance for all courses
2. New grading scale with plus/minus grades for all departments
3. Revised academic integrity policy with stricter penalties for violations
4. Mandatory academic advising for all students with less than a 2.5 GPA
5. New course evaluation system with real-time feedback options

The attendance policy will now require students to attend at least 90% of all scheduled classes. Students who fall below this threshold may be subject to academic probation or course withdrawal. Exceptions will be made for documented medical or family emergencies.

The new grading scale will provide more detailed feedback on student performance. Plus and minus grades will be awarded for all letter grades except A+, which will remain the highest possible grade. This change aligns with practices at peer institutions and provides better differentiation of student achievement.

The academic integrity policy has been strengthened to address new forms of academic misconduct, including unauthorized use of AI tools and online collaboration platforms. Students found in violation will face more severe consequences, including potential suspension for repeat offenses.

Students with cumulative GPAs below 2.5 will be required to meet with an academic advisor each semester to develop and monitor academic improvement plans. This proactive approach aims to identify and support struggling students before they face academic dismissal.

The new course evaluation system will allow students to provide feedback throughout the semester rather than only at the end. This real-time feedback will enable instructors to adjust their teaching methods and course content to better meet student needs.

These changes will be effective for the Spring semester registration period beginning November 15th. Students are encouraged to review the complete policy documents on the university website and contact their academic advisors with any questions.

Additional resources and support services will be available to help students adapt to these new policies. The university remains committed to providing a high-quality education while maintaining the highest standards of academic excellence and integrity.''',
                'is_published': True
            },
            {
                'title': 'Campus Sustainability Initiative Launch',
                'content': '''The university is proud to announce the launch of our comprehensive Campus Sustainability Initiative, a multi-year program designed to reduce our environmental impact and promote sustainable practices across all campus operations.

Phase 1 of the initiative includes:
- Installation of solar panels on all academic buildings
- Implementation of a comprehensive recycling and composting program
- Conversion of campus vehicle fleet to electric or hybrid models
- Construction of LEED-certified buildings for new construction projects
- Establishment of a campus sustainability office with dedicated staff

The solar panel installation will begin in January and is expected to reduce our carbon footprint by 40% within the first year. All academic buildings will be equipped with photovoltaic systems capable of generating 75% of each building's energy needs.

Our new recycling and composting program will divert 85% of campus waste from landfills. Special collection points will be placed throughout campus, and educational workshops will be offered to help students and staff participate effectively.

The campus vehicle fleet will transition to electric and hybrid models over the next 24 months. This includes shuttle buses, maintenance vehicles, and administrative cars. Charging stations will be installed in all parking areas to support this transition.

All new construction projects must meet LEED Gold certification standards or higher. Our first LEED-certified building, the new Engineering Innovation Center, is scheduled for completion in Fall 2026.

The campus sustainability office will coordinate all initiatives and provide resources for student and faculty research projects related to environmental sustainability. The office will also manage our carbon offset programs and sustainability reporting.

Student involvement is crucial to the success of this initiative. We will be launching several student organizations and internship opportunities focused on sustainability projects. Students interested in participating should contact the sustainability office or visit our website for more information.

Funding for Phase 1 of the initiative comes from a combination of university resources, state grants, and private donations. We anticipate that energy savings and other efficiencies will offset initial costs within five years.

We believe this initiative demonstrates our commitment to environmental stewardship and prepares our students to be leaders in sustainability in their future careers. Together, we can make our campus a model for sustainable higher education institutions.

Regular progress reports will be published on our sustainability website, and we encourage the entire university community to participate in making our campus more environmentally responsible.''',
                'is_published': True
            }
        ]

        for data in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'is_published': data['is_published']
                }
            )
            if created:
                self.stdout.write(
                    'Successfully created announcement: %s' % announcement.title
                )
            else:
                self.stdout.write(
                    'Announcement already exists: %s' % announcement.title
                )