from typing import TYPE_CHECKING
from django.db import models
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
