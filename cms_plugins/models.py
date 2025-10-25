from typing import TYPE_CHECKING
from django.db import models
from django.db.models import Q
from cms.models.pluginmodel import CMSPlugin

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from cms_plugins.models import Announcement, QuickLinkItem, StatisticsCounterItem
    from django.db.models.manager import Manager

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published: bool = models.BooleanField(default=True)  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
    
    def __str__(self) -> str:
        return str(self.title)

class Event(models.Model):
    EVENT_CATEGORIES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('social', 'Social'),
        ('administrative', 'Administrative'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES, default='academic')
    is_published: bool = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self) -> str:
        return str(self.title)

class Course(models.Model):
    COURSE_CATEGORIES = [
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('business', 'Business'),
        ('technology', 'Technology'),
    ]
    
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=COURSE_CATEGORIES, default='science')
    instructor = models.CharField(max_length=100)
    credits: int = models.PositiveIntegerField(default=3)  # type: ignore
    duration = models.CharField(max_length=50, help_text="e.g., '15 weeks', '8 weeks'")
    is_published: bool = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['title']
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self) -> str:
        return f"{self.code} - {self.title}"

# Add the Student and Grade models
class Student(models.Model):
    """
    Model representing a student in the system.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()
    is_active: bool = models.BooleanField(default=True)  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Grade(models.Model):
    """
    Model representing a student's grade for a course.
    """
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
        ('F', 'F'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    date_recorded = models.DateField(auto_now_add=True)
    semester = models.CharField(max_length=20, help_text="e.g., 'Fall 2023', 'Spring 2024'")
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['-date_recorded']
        unique_together = ['student', 'course']
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
    
    def __str__(self) -> str:
        return f"{self.student} - {self.course} - {self.grade}"

class Enrollment(models.Model):
    """
    Model representing a student's enrollment in a course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active: bool = models.BooleanField(default=True)  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['student', 'course']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
    
    def __str__(self) -> str:
        return f"{self.student} enrolled in {self.course}"

class Attendance(models.Model):
    """
    Model representing a student's attendance record for a course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    is_present: bool = models.BooleanField(default=True)  # type: ignore
    is_excused: bool = models.BooleanField(default=False)  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'course', 'date']
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
    
    def __str__(self) -> str:
        status = "Present" if self.is_present else "Absent"
        if self.is_excused:
            status += " (Excused)"
        return f"{self.student} - {self.course} - {self.date} - {status}"

class StudentDashboardPlugin(CMSPlugin):
    """
    A plugin to display personalized student information including:
    - Enrolled courses
    - Attendance percentage
    - Recent grades
    """
    title = models.CharField(max_length=200, default="My Dashboard")
    
    def __str__(self) -> str:
        return str(self.title)
    
    def get_student_data(self, student_id=None):
        """
        Fetch student data for the dashboard.
        In a real implementation, this would likely get the student ID from the session
        or request context. For now, we'll return sample data or data for a specific student.
        """
        from django.core.cache import cache
        from django.db.models import Count, Q
        from django.utils import timezone
        
        # Create a cache key
        cache_key = f"student_dashboard_{student_id or 'sample'}"
        
        # Try to get data from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # If no student_id provided, return empty data
        if not student_id:
            data = {
                'student': {
                    'name': '',
                    'student_id': '',
                    'email': ''
                },
                'enrolled_courses': [],
                'attendance_percentage': 0,
                'recent_grades': []
            }
        else:
            try:
                # Get the student
                student = Student.objects.get(student_id=student_id)
                
                # Get enrolled courses
                enrollments = Enrollment.objects.filter(
                    student=student, 
                    is_active=True
                ).select_related('course')
                
                enrolled_courses = []
                total_attendance = 0
                attendance_count = 0
                
                for enrollment in enrollments:
                    # Calculate progress (simplified)
                    progress = 50  # This would be calculated based on actual course progress
                    
                    # Calculate attendance percentage for this course
                    total_records = Attendance.objects.filter(
                        student=student,
                        course=enrollment.course
                    ).count()
                    
                    if total_records > 0:
                        present_records = Attendance.objects.filter(
                            student=student,
                            course=enrollment.course,
                            is_present=True
                        ).count()
                        
                        course_attendance = (present_records / total_records) * 100
                        total_attendance += course_attendance
                        attendance_count += 1
                    else:
                        course_attendance = 0
                    
                    enrolled_courses.append({
                        'id': enrollment.course.id,
                        'title': enrollment.course.title,
                        'code': enrollment.course.code,
                        'instructor': enrollment.course.instructor,
                        'progress': progress,
                        'attendance': round(course_attendance, 1)
                    })
                
                # Calculate overall attendance percentage
                if attendance_count > 0:
                    attendance_percentage = total_attendance / attendance_count
                else:
                    attendance_percentage = 0
                
                # Get recent grades (last 5)
                recent_grades = []
                grades = Grade.objects.filter(
                    student=student
                ).select_related('course').order_by('-date_recorded')[:5]
                
                for grade in grades:
                    recent_grades.append({
                        'course': grade.course.title,
                        'course_code': grade.course.code,
                        'grade': grade.grade,
                        'date': grade.date_recorded.strftime('%Y-%m-%d')
                    })
                
                data = {
                    'student': {
                        'name': student.full_name,
                        'student_id': student.student_id,
                        'email': student.email
                    },
                    'enrolled_courses': enrolled_courses,
                    'attendance_percentage': round(attendance_percentage, 1),
                    'recent_grades': recent_grades
                }
            except Exception:
                # Return empty data if student not found or any other error
                data = {
                    'student': {
                        'name': '',
                        'student_id': '',
                        'email': ''
                    },
                    'enrolled_courses': [],
                    'attendance_percentage': 0,
                    'recent_grades': []
                }
        
        # Cache the data for 10 minutes
        cache.set(cache_key, data, 600)  # 600 seconds = 10 minutes
        
        return data

class HeroBannerPlugin(CMSPlugin):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='hero_banners/', blank=True)
    background_video = models.FileField(upload_to='hero_banners/', blank=True, help_text="MP4 format recommended")
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.URLField(blank=True)
    width: int = models.PositiveIntegerField(default=1200, help_text="Width in pixels")  # type: ignore
    height: int = models.PositiveIntegerField(default=400, help_text="Height in pixels")  # type: ignore
    # Custom styling options
    background_color = models.CharField(max_length=7, default="#ffffff", help_text="Background color in hex format (e.g., #ffffff)")
    text_color = models.CharField(max_length=7, default="#000000", help_text="Text color in hex format (e.g., #000000)")
    font_size: int = models.PositiveIntegerField(default=16, help_text="Font size in pixels")  # type: ignore
    # Overlay gradient options
    overlay_color = models.CharField(max_length=7, default="#000000", help_text="Overlay color in hex format (e.g., #000000)")
    overlay_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.8, help_text="Overlay opacity (0.0 to 1.0)")
    
    def __str__(self) -> str:
        return str(self.title)

class FeaturedAnnouncementsPlugin(CMSPlugin):
    title = models.CharField(max_length=200, default="Latest Announcements")  # type: ignore
    number_of_items: int = models.PositiveIntegerField(default=3)  # type: ignore
    enable_carousel: bool = models.BooleanField(default=True, help_text="Enable carousel view for announcements")  # type: ignore
    
    def get_announcements(self):
        """
        Returns the latest 'number_of_items' published announcements
        ordered by creation date descending.
        """
        from cms_plugins.models import Announcement
        return Announcement.objects.filter(
            is_published=True
        ).order_by('-created_at')[:self.number_of_items]
    
    def get_announcements_data(self):
        """
        Returns announcements data in a format suitable for AJAX requests.
        """
        from cms_plugins.models import Announcement
        from django.utils import dateformat
        
        announcements = self.get_announcements()
        data = []
        for i, announcement in enumerate(announcements):
            data.append({
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'created_at': dateformat.format(announcement.created_at, 'F d, Y'),
                'is_featured': i == 0  # First announcement is featured
            })
        return data
    
    def __str__(self) -> str:
        return str(self.title)

class UpcomingEventsPlugin(CMSPlugin):
    title = models.CharField(max_length=200, default="Upcoming Events")  # type: ignore
    number_of_items: int = models.PositiveIntegerField(default=5)  # type: ignore
    show_past_events: bool = models.BooleanField(default=False)  # type: ignore
    enable_carousel: bool = models.BooleanField(default=True, help_text="Enable carousel view for events")  # type: ignore
    auto_rotate: bool = models.BooleanField(default=True, help_text="Enable automatic rotation of events in carousel")  # type: ignore
    rotation_interval: int = models.PositiveIntegerField(default=5000, help_text="Rotation interval in milliseconds (minimum 1000)")  # type: ignore
    show_category_filter: bool = models.BooleanField(default=True, help_text="Show category filter dropdown")  # type: ignore
    show_date_filter: bool = models.BooleanField(default=True, help_text="Show date filter dropdown")  # type: ignore
    
    def get_events(self, category='', date_filter=''):
        """
        Fetches upcoming events from the Event model with optional filtering.
        """
        from cms_plugins.models import Event
        from django.utils import timezone
        
        # Start with base query
        events_query = Event.objects.filter(is_published=True)
        
        # Get current time for date filtering
        now = timezone.now()
        
        # Apply category filter if provided
        if category:
            events_query = events_query.filter(category=category)
        
        # Apply date filter if provided
        if date_filter:
            if date_filter == 'today':
                events_query = events_query.filter(start_date__date=now.date())
            elif date_filter == 'this_week':
                week_start = now - timezone.timedelta(days=now.weekday())
                week_end = week_start + timezone.timedelta(days=6)
                events_query = events_query.filter(start_date__date__range=[week_start.date(), week_end.date()])
            elif date_filter == 'this_month':
                events_query = events_query.filter(
                    start_date__year=now.year,
                    start_date__month=now.month
                )
        
        # Apply past events filter
        if not self.show_past_events:
            events_query = events_query.filter(start_date__gte=now)
        
        # Apply ordering and limit
        return events_query.order_by('start_date')[:self.number_of_items]
    
    def get_events_data(self, category='', date_filter=''):
        """
        Returns events data in a format suitable for AJAX requests.
        """
        from cms_plugins.models import Event
        from django.utils import dateformat
        from django.utils import timezone
        
        events = self.get_events(category, date_filter)
        data = []
        now = timezone.now()
        for event in events:
            data.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start_date': dateformat.format(event.start_date, 'F d, Y \a\t g:i A'),
                'end_date': dateformat.format(event.end_date, 'F d, Y \a\t g:i A') if event.end_date else None,
                'location': event.location,
                'category': event.get_category_display(),
                'category_key': event.category,
                'is_future': event.start_date >= now,
            })
        return data
    
    def __str__(self) -> str:
        return str(self.title)

class WelcomeSectionPlugin(CMSPlugin):
    IMAGE_ALIGNMENT_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
        ('background', 'Full-width Background'),
    ]
    
    heading = models.CharField(max_length=200)
    content = models.TextField(help_text="Supports HTML formatting")
    image = models.ImageField(upload_to='welcome_images/', blank=True)
    image_alignment = models.CharField(
        max_length=20,
        choices=IMAGE_ALIGNMENT_CHOICES,
        default='right',
        help_text="Select image alignment"
    )
    cta_text = models.CharField(max_length=100, blank=True, help_text="Text for the call-to-action button")
    cta_link = models.URLField(blank=True, help_text="URL for the call-to-action button")
    
    def __str__(self) -> str:
        return str(self.heading)

class QuickLinksPlugin(CMSPlugin):
    """
    A plugin that contains multiple quick link items.
    """
    
    def copy_relations(self, old_instance):
        # Copy the related link items when copying the plugin
        for link_item in old_instance.quicklinkitem_set.all():
            link_item.pk = None  # Reset the primary key to create a new object
            link_item.quick_links_plugin = self  # Set the new plugin instance
            link_item.save()
    
    def __str__(self) -> str:
        # Use a more direct approach to count the links
        if TYPE_CHECKING:
            # This is just for type checking, the actual count will be done differently
            return "Quick Links"
        else:
            # In runtime, we can access the related manager
            return f"Quick Links ({self.quicklinkitem_set.count()} link{'s' if self.quicklinkitem_set.count() != 1 else ''})"

class QuickLinkItem(models.Model):
    """
    An individual link item within a QuickLinksPlugin.
    """
    quick_links_plugin = models.ForeignKey(QuickLinksPlugin, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True, help_text="Optional icon class (e.g., 'fa fa-home')")
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    background_color = models.CharField(max_length=7, default="#ffffff", help_text="Background color in hex format (e.g., #ffffff)")
    order: int = models.PositiveIntegerField(default=0, help_text="Order of the link in the plugin")  # type: ignore
    
    class Meta:
        ordering = ['order']
        verbose_name = "Quick Link Item"
        verbose_name_plural = "Quick Link Items"
    
    def __str__(self) -> str:
        return str(self.title)

class StatisticsCounterPlugin(CMSPlugin):
    """
    A plugin that contains multiple statistics counters.
    """
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    def copy_relations(self, old_instance):
        # Copy the related counter items when copying the plugin
        for counter_item in old_instance.statisticscounteritem_set.all():
            counter_item.pk = None  # Reset the primary key to create a new object
            counter_item.statistics_counter_plugin = self  # Set the new plugin instance
            counter_item.save()
    
    def __str__(self) -> str:
        # Use a more direct approach to count the counters
        if TYPE_CHECKING:
            # This is just for type checking, the actual count will be done differently
            return "Statistics Counters"
        else:
            # In runtime, we can access the related manager
            count = self.statisticscounteritem_set.count()
            return f"Statistics Counters ({count} counter{'s' if count != 1 else ''})"

class StatisticsCounterItem(models.Model):
    """
    An individual counter item within a StatisticsCounterPlugin.
    """
    statistics_counter_plugin = models.ForeignKey(StatisticsCounterPlugin, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value: int = models.PositiveIntegerField()  # type: ignore
    icon = models.CharField(max_length=50, blank=True, help_text="Optional icon class (e.g., 'fa fa-users')")
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['pk']
        verbose_name = "Statistics Counter Item"
        verbose_name_plural = "Statistics Counter Items"
    
    def __str__(self) -> str:
        return f"{self.label}: {self.value}"

class TestimonialPlugin(CMSPlugin):
    """
    A plugin that contains multiple testimonials.
    """
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    def copy_relations(self, old_instance):
        # Copy the related testimonial items when copying the plugin
        for testimonial_item in old_instance.testimonialitem_set.all():
            testimonial_item.pk = None  # Reset the primary key to create a new object
            testimonial_item.testimonial_plugin = self  # Set the new plugin instance
            testimonial_item.save()
    
    def __str__(self) -> str:
        # Return the name of the first testimonial or a default message
        if TYPE_CHECKING:
            # This is just for type checking
            return "Testimonials"
        else:
            # In runtime, we can access the related manager
            first_testimonial = self.testimonialitem_set.first()
            if first_testimonial:
                return str(first_testimonial.name)
            return "No testimonials"

class TestimonialItem(models.Model):
    """
    An individual testimonial within a TestimonialPlugin.
    """
    testimonial_plugin = models.ForeignKey(TestimonialPlugin, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    course = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    is_featured: bool = models.BooleanField(default=False, help_text="Highlight this testimonial")  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['pk']
        verbose_name = "Testimonial Item"
        verbose_name_plural = "Testimonial Items"
    
    def __str__(self) -> str:
        return str(self.name)

class CTABannerPlugin(CMSPlugin):
    """
    A Call-to-Action banner plugin for the homepage.
    """
    heading = models.CharField(max_length=200)
    subheading = models.TextField(blank=True)
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.URLField(blank=True)
    background_image = models.ImageField(upload_to='cta_banners/', blank=True)
    background_color = models.CharField(max_length=7, default="#007bff", help_text="Background color in hex format (e.g., #007bff)")
    
    def __str__(self) -> str:
        return str(self.heading)

class CourseSearchPlugin(CMSPlugin):
    """
    A plugin for course search functionality.
    """
    title = models.CharField(max_length=200, default="Course Search")
    placeholder_text = models.CharField(max_length=200, default="Search courses by title, code, description, or instructor...")
    
    def __str__(self) -> str:
        return str(self.title)

class NavbarPlugin(CMSPlugin):
    """
    A plugin for editable navigation bar.
    """
    brand_text = models.CharField(max_length=200, default="Student Management System")
    brand_link = models.CharField(max_length=200, default="/", help_text="URL for the brand/logo link")
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    def __str__(self) -> str:
        return str(self.brand_text)

    def get_menu_items(self):
        """
        Returns menu items for the navbar.
        """
        if TYPE_CHECKING:
            # This is just for type checking
            return []
        else:
            # In runtime, we can access the related manager
            return NavbarItem.objects.filter(navbar_plugin=self).order_by('order')

class NavbarItem(models.Model):
    """
    Individual menu items for the navbar.
    """
    navbar_plugin = models.ForeignKey(NavbarPlugin, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, help_text="URL for the menu item (leave blank for dropdown)")
    order: int = models.PositiveIntegerField(default=0, help_text="Order of the item in the navbar")  # type: ignore
    is_active: bool = models.BooleanField(default=False, help_text="Mark as active item")  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['order']
        verbose_name = "Navbar Item"
        verbose_name_plural = "Navbar Items"
    
    def __str__(self) -> str:
        return str(self.title)

    def get_children(self):
        """
        Returns child menu items (for dropdowns).
        """
        if TYPE_CHECKING:
            # This is just for type checking
            return []
        else:
            # In runtime, we can access the related manager
            return NavbarItemChild.objects.filter(parent=self).order_by('order')

class NavbarItemChild(models.Model):
    """
    Child menu items for dropdowns in the navbar.
    """
    parent = models.ForeignKey(NavbarItem, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order: int = models.PositiveIntegerField(default=0)  # type: ignore
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['order']
        verbose_name = "Navbar Child Item"
        verbose_name_plural = "Navbar Child Items"
    
    def __str__(self) -> str:
        return str(self.title)

class LiveNotification(models.Model):
    """
    Model representing a live notification for students.
    """
    CATEGORY_CHOICES = [
        ('announcement', 'New Announcement'),
        ('grade', 'Grade Released'),
        ('event', 'Event Reminder'),
        ('system', 'System Notification'),
    ]
    
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='system')
    is_read = models.BooleanField(default=False)  # type: ignore
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    
    # Type annotation for the objects manager to help type checkers
    if TYPE_CHECKING:
        objects: 'Manager'
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Live Notification"
        verbose_name_plural = "Live Notifications"
    
    def __str__(self) -> str:
        message_str = str(self.message)
        return f"{message_str[:50]}..." if len(message_str) > 50 else message_str
    
    def mark_as_read(self) -> None:
        """
        Mark the notification as read.
        """
        self.is_read = True
        self.save()

class LiveNotificationsPlugin(CMSPlugin):
    """
    A plugin to display live notifications for students.
    """
    title = models.CharField(max_length=200, default="Notifications")
    
    def __str__(self) -> str:
        return str(self.title)
    
    def get_unread_count(self, user) -> int:
        """
        Get the count of unread notifications for a user.
        """
        if user.is_authenticated:
            return LiveNotification.objects.filter(user=user, is_read=False).count()
        return 0
    
    def get_notifications(self, user, limit=10) -> list:
        """
        Get the latest notifications for a user.
        """
        if user.is_authenticated:
            notifications = LiveNotification.objects.filter(user=user)[:limit]
            return [
                {
                    'id': notification.id,
                    'message': notification.message,
                    'category': notification.get_category_display(),
                    'category_key': notification.category,
                    'is_read': notification.is_read,
                    'timestamp': notification.timestamp.isoformat(),
                }
                for notification in notifications
            ]
        return []

class PerformanceAnalyticsPlugin(CMSPlugin):
    """
    A plugin to display student performance analytics with charts.
    """
    title = models.CharField(max_length=200, default="Performance Analytics")
    TIME_RANGE_CHOICES = [
        ('week', 'Weekly'),
        ('month', 'Monthly'),
        ('semester', 'Semester'),
    ]
    default_time_range = models.CharField(
        max_length=10, 
        choices=TIME_RANGE_CHOICES, 
        default='month',
        help_text="Default time range for analytics"
    )
    
    def __str__(self) -> str:
        return str(self.title)
    
    def get_chart_data(self, user, time_range=None) -> dict:
        """
        Get aggregated performance data for charts.
        """
        if not user.is_authenticated:
            return {}
        
        # Use default time range if none provided
        if time_range is None:
            time_range = self.default_time_range
            
        # Import here to avoid circular imports
        from django.utils import timezone
        from datetime import timedelta
        from .models import Grade, Attendance, Student, Course, Enrollment
        
        try:
            # Get the student record for this user
            student = Student.objects.get(email=user.email)
        except Student.DoesNotExist:  # type: ignore
            # If no student record found, return empty data
            return {
                'academic_performance': [],
                'attendance_rate': [],
                'activity_trends': []
            }
        
        # Calculate date range based on time_range
        end_date = timezone.now().date()
        if time_range == 'week':
            start_date = end_date - timedelta(days=7)
        elif time_range == 'month':
            start_date = end_date - timedelta(days=30)
        else:  # semester
            start_date = end_date - timedelta(days=180)
        
        # Get academic performance data (grades over time)
        grades = Grade.objects.filter(
            student=student,
            date_recorded__range=[start_date, end_date]
        ).order_by('date_recorded')
        
        academic_performance = []
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        
        for grade in grades:
            academic_performance.append({
                'date': grade.date_recorded.isoformat(),
                'course': grade.course.title,
                'grade': grade.grade,
                'points': grade_points.get(grade.grade, 0)
            })
        
        # Get attendance data
        enrollments = Enrollment.objects.filter(student=student)
        course_ids = [e.course.id for e in enrollments]
        
        attendance_records = Attendance.objects.filter(
            student=student,
            course_id__in=course_ids,
            date__range=[start_date, end_date]
        )
        
        # Group attendance by date
        attendance_by_date = {}
        for record in attendance_records:
            date_str = record.date.isoformat()
            if date_str not in attendance_by_date:
                attendance_by_date[date_str] = {'present': 0, 'total': 0}
            attendance_by_date[date_str]['total'] += 1
            if record.is_present:
                attendance_by_date[date_str]['present'] += 1
        
        attendance_rate = []
        for date, counts in attendance_by_date.items():
            rate = (counts['present'] / counts['total']) * 100 if counts['total'] > 0 else 0
            attendance_rate.append({
                'date': date,
                'rate': round(rate, 2),
                'present': counts['present'],
                'total': counts['total']
            })
        
        # Activity trends (number of activities per day)
        # For simplicity, we'll use grades and attendance as activities
        activity_trends = []
        all_dates = set()
        all_dates.update([g.date_recorded.isoformat() for g in grades])
        all_dates.update([a.date.isoformat() for a in attendance_records])
        
        for date in sorted(all_dates):
            grade_count = len([g for g in grades if g.date_recorded.isoformat() == date])
            attendance_count = len([a for a in attendance_records if a.date.isoformat() == date])
            activity_trends.append({
                'date': date,
                'activities': grade_count + attendance_count
            })
        
        return {
            'academic_performance': academic_performance,
            'attendance_rate': attendance_rate,
            'activity_trends': activity_trends,
            'time_range': time_range
        }


class AttendanceTrackerPlugin(CMSPlugin):
    """
    A plugin to track and update student attendance in real time.
    """
    title = models.CharField(max_length=200, default="Attendance Tracker")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, 
                               help_text="Select a course to track attendance for. If none selected, shows all courses.")
    date = models.DateField(help_text="Date for which to track attendance")
    
    def __str__(self) -> str:
        return str(self.title)
    
    def get_attendance_data(self, search_query=''):
        """
        Get attendance data for the specified course and date.
        If no course is specified, get data for all courses.
        """
        
        # Get enrollments for the course(s)
        enrollments = Enrollment.objects.filter(is_active=True)
        
        if self.course:
            enrollments = enrollments.filter(course=self.course)
        
        # Apply search filter if provided
        if search_query:
            # Using union of separate queries to avoid type checking errors with Q objects
            enrollments = (enrollments.filter(student__first_name__icontains=search_query)
                         .union(enrollments.filter(student__last_name__icontains=search_query))
                         .union(enrollments.filter(course__title__icontains=search_query))
                         .union(enrollments.filter(course__code__icontains=search_query)))
        
        # Get existing attendance records for this date
        enrollment_ids = [e.id for e in enrollments]
        existing_attendance = Attendance.objects.filter(
            student__enrollment__in=enrollment_ids,
            date=self.date
        )
        
        # Create a mapping of student_id_course_id to attendance status
        attendance_map = {}
        for record in existing_attendance:
            key = f"{record.student.id}_{record.course.id}"
            attendance_map[key] = {
                'id': record.id,
                'is_present': record.is_present,
                'is_excused': record.is_excused
            }
        
        # Build the data structure
        attendance_data = []
        for enrollment in enrollments:
            key = f"{enrollment.student.id}_{enrollment.course.id}"
            attendance_record = attendance_map.get(key, None)
            
            attendance_data.append({
                'enrollment_id': enrollment.id,
                'student_id': enrollment.student.id,
                'student_name': enrollment.student.full_name,
                'course_id': enrollment.course.id,
                'course_name': enrollment.course.title,
                'course_code': enrollment.course.code,
                'attendance_id': attendance_record['id'] if attendance_record else None,
                'is_present': attendance_record['is_present'] if attendance_record else True,
                'is_excused': attendance_record['is_excused'] if attendance_record else False
            })
        
        # Calculate completion percentage
        total_students = len(attendance_data)
        marked_present = sum(1 for item in attendance_data if item['is_present'])
        completion_percentage = (marked_present / total_students * 100) if total_students > 0 else 0
        
        return {
            'attendance_data': attendance_data,
            'completion_percentage': round(completion_percentage, 1),
            'total_students': total_students,
            'marked_present': marked_present
        }

class StudyRecommendationPlugin(CMSPlugin):
    """
    A plugin to recommend study materials or courses based on student grades and interests.
    """
    title = models.CharField(max_length=200, default="Recommended Study Materials")
    
    # Recommendation settings
    NUMBER_OF_RECOMMENDATIONS_CHOICES = [
        (3, '3 Recommendations'),
        (5, '5 Recommendations'),
        (10, '10 Recommendations'),
    ]
    number_of_recommendations: int = models.PositiveIntegerField(
        choices=NUMBER_OF_RECOMMENDATIONS_CHOICES, 
        default=5,
        help_text="Number of recommendations to display"
    )  # type: ignore
    
    def __str__(self) -> str:
        return str(self.title)
    
    def get_recommendations(self, student=None, difficulty_filter='', subject_filter=''):
        """
        Get study material recommendations based on student grades and interests.
        Uses a weighted scoring algorithm to rank materials.
        """
        from .utils import calculate_recommendation_score
        
        # Get all courses that are published
        courses_query = Course.objects.filter(is_published=True)
        
        # Apply filters if provided
        if subject_filter:
            courses_query = courses_query.filter(category=subject_filter)
            
        # Convert queryset to list for processing
        courses = list(courses_query)
        
        # Calculate scores for each course
        scored_courses = []
        for course in courses:
            # Calculate recommendation score
            score = calculate_recommendation_score(student, course, difficulty_filter)
            
            # Only include courses with positive scores
            if score > 0:
                scored_courses.append({
                    'course': course,
                    'score': score,
                    'difficulty_level': self._get_difficulty_level(course)
                })
        
        # Sort by score (descending)
        scored_courses.sort(key=lambda x: x['score'], reverse=True)
        
        # Limit to requested number of recommendations
        recommendations = scored_courses[:self.number_of_recommendations]
        
        # Format for JSON response
        formatted_recommendations = []
        for item in recommendations:
            course = item['course']
            formatted_recommendations.append({
                'id': course.id,
                'title': course.title,
                'code': course.code,
                'description': course.description,
                'instructor': course.instructor,
                'category': course.get_category_display(),
                'category_key': course.category,
                'credits': course.credits,
                'difficulty_level': item['difficulty_level'],
                'score': round(item['score'], 2),
                'link': f"/courses/{course.id}/"  # Adjust URL pattern as needed
            })
        
        return formatted_recommendations
    
    def _get_difficulty_level(self, course):
        """
        Determine difficulty level based on course credits and category.
        """
        # Simple heuristic: higher credits = higher difficulty
        if course.credits >= 4:
            return "Advanced"
        elif course.credits >= 3:
            return "Intermediate"
        else:
            return "Beginner"
    
    def get_subject_choices(self):
        """
        Return available subject categories for filtering.
        """
        return Course.COURSE_CATEGORIES
    
    def get_difficulty_choices(self):
        """
        Return available difficulty levels for filtering.
        """
        return [
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')
        ]
