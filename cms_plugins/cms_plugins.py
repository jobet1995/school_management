from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.contrib import admin

from .models import (
    HeroBannerPlugin, 
    FeaturedAnnouncementsPlugin, 
    UpcomingEventsPlugin, 
    WelcomeSectionPlugin, 
    QuickLinksPlugin, 
    QuickLinkItem, 
    StatisticsCounterPlugin, 
    StatisticsCounterItem, 
    TestimonialPlugin, 
    TestimonialItem, 
    CTABannerPlugin, 
    CourseSearchPlugin,
    NavbarPlugin,
    NavbarItem,
    NavbarItemChild,
    StudentDashboardPlugin,
    LiveNotificationsPlugin,
    PerformanceAnalyticsPlugin,  # Add our new plugin model
    AttendanceTrackerPlugin,
    StudyRecommendationPlugin  # Add our new plugin model
)


class QuickLinkItemInline(admin.StackedInline):
    model = QuickLinkItem
    extra = 1
    fields = ('icon', 'title', 'description', 'link', 'background_color', 'order')


class StatisticsCounterItemInline(admin.StackedInline):
    model = StatisticsCounterItem
    extra = 1
    fields = ('label', 'value', 'icon')


class TestimonialItemInline(admin.StackedInline):
    model = TestimonialItem
    extra = 1
    fields = ('name', 'photo', 'course', 'testimonial', 'is_featured')


class NavbarItemChildInline(admin.StackedInline):
    model = NavbarItemChild
    extra = 1
    fields = ('title', 'url', 'order')


class NavbarItemInline(admin.StackedInline):
    model = NavbarItem
    extra = 1
    fields = ('title', 'url', 'order', 'is_active')
    inlines = [NavbarItemChildInline]


@plugin_pool.register_plugin
class NavbarPluginPublisher(CMSPluginBase):
    model = NavbarPlugin
    name = _("Navbar Plugin")
    render_template = "navbar_plugin.html"
    cache = False
    inlines = [NavbarItemInline]
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['menu_items'] = instance.get_menu_items()
        return context


@plugin_pool.register_plugin
class HeroBannerPluginPublisher(CMSPluginBase):
    model = HeroBannerPlugin
    name = _("Hero Banner Plugin")
    render_template = "hero_banner_plugin.html"
    cache = False
    # Allow the plugin to be resizable
    resizable = True
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'subtitle',
                ('background_image', 'background_video'),
                ('cta_text', 'cta_link'),
            )
        }),
        (_('Dimensions'), {
            'fields': (
                'width',
                'height',
            ),
            'classes': ('collapse',),
        }),
        (_('Styling'), {
            'fields': (
                'background_color',
                'text_color',
                'font_size',
            ),
            'classes': ('collapse',),
        }),
        (_('Overlay'), {
            'fields': (
                'overlay_color',
                'overlay_opacity',
            ),
            'classes': ('collapse',),
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/admin/cms_plugins_admin.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class FeaturedAnnouncementsPluginPublisher(CMSPluginBase):
    model = FeaturedAnnouncementsPlugin
    name = _("Featured Announcements Plugin")
    render_template = "featured_announcements_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'number_of_items',
                'enable_carousel',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/featured_announcements.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/featured_announcements.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # We're loading announcements via AJAX, so we don't need to pass them in the context
        context['enable_carousel'] = instance.enable_carousel
        return context

@plugin_pool.register_plugin
class UpcomingEventsPluginPublisher(CMSPluginBase):
    model = UpcomingEventsPlugin
    name = _("Upcoming Events Plugin")
    render_template = "upcoming_events_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'number_of_items',
                'show_past_events',
            )
        }),
        (_('Carousel Settings'), {
            'fields': (
                'enable_carousel',
                'auto_rotate',
                'rotation_interval',
            ),
            'classes': ('collapse',),
        }),
        (_('Filter Settings'), {
            'fields': (
                'show_category_filter',
                'show_date_filter',
            ),
            'classes': ('collapse',),
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/upcoming_events.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/upcoming_events.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # We're loading events via AJAX, so we don't need to pass them in the context
        context['enable_carousel'] = instance.enable_carousel
        context['auto_rotate'] = instance.auto_rotate
        context['rotation_interval'] = instance.rotation_interval
        return context

@plugin_pool.register_plugin
class WelcomeSectionPluginPublisher(CMSPluginBase):
    model = WelcomeSectionPlugin
    name = _("Welcome Section Plugin")
    render_template = "welcome_section_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'heading',
                'content',
                'image',
                'image_alignment',
                ('cta_text', 'cta_link'),
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/welcome_section.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/welcome_section.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['image_alignment'] = instance.image_alignment
        return context

@plugin_pool.register_plugin
class QuickLinksPluginPublisher(CMSPluginBase):
    model = QuickLinksPlugin
    name = _("Quick Links Plugin")
    render_template = "quick_links_plugin.html"
    cache = False
    inlines = [QuickLinkItemInline]
    
    class Media:
        css = {
            'all': (
                static('css/quick_links.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/quick_links.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['links'] = instance.quicklinkitem_set.all().order_by('order')
        return context

@plugin_pool.register_plugin
class StatisticsCounterPluginPublisher(CMSPluginBase):
    model = StatisticsCounterPlugin
    name = _("Statistics Counter Plugin")
    render_template = "statistics_counter_plugin.html"
    cache = False
    inlines = [StatisticsCounterItemInline]
    
    class Media:
        css = {
            'all': (
                static('css/statistics_counter.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/statistics_counter.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['counters'] = instance.statisticscounteritem_set.all()
        return context

@plugin_pool.register_plugin
class TestimonialPluginPublisher(CMSPluginBase):
    model = TestimonialPlugin
    name = _("Testimonial Plugin")
    render_template = "testimonial_plugin.html"
    cache = False
    inlines = [TestimonialItemInline]
    
    class Media:
        css = {
            'all': (
                static('css/testimonial.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/testimonial.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['testimonials'] = instance.testimonialitem_set.all()
        context['featured_testimonials'] = instance.testimonialitem_set.filter(is_featured=True)
        return context

@plugin_pool.register_plugin
class CTABannerPluginPublisher(CMSPluginBase):
    model = CTABannerPlugin
    name = _("CTA Banner Plugin")
    render_template = "cta_banner_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'heading',
                'subheading',
                'background_image',
                'background_color',
                ('cta_text', 'cta_link'),
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/cta_banner.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/cta_banner.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class CourseSearchPluginPublisher(CMSPluginBase):
    model = CourseSearchPlugin
    name = _("Course Search Plugin")
    render_template = "course_search_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'placeholder_text',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/course_search.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/course_search.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class StudentDashboardPluginPublisher(CMSPluginBase):
    model = StudentDashboardPlugin
    name = _("Student Dashboard Plugin")
    render_template = "student_dashboard_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/student_dashboard.css'),
                static('css/loading_spinner.css'),  # Add loading spinner CSS
            )
        }
        js = (
            static('js/student_dashboard.js'),
            static('js/loading_spinner.js'),  # Add loading spinner JS
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # Get student data (in a real implementation, you would get the student ID from the session)
        student_data = instance.get_student_data()
        context['student_data'] = student_data
        return context

@plugin_pool.register_plugin
class LiveNotificationsPluginPublisher(CMSPluginBase):
    model = LiveNotificationsPlugin
    name = _("Live Notifications Plugin")
    render_template = "live_notifications_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/live_notifications.css'),
            )
        }
        js = (
            static('js/live_notifications.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # Get the current user from the request
        request = context['request']
        user = request.user
        
        # Get unread count and notifications
        unread_count = instance.get_unread_count(user)
        notifications = instance.get_notifications(user)
        
        context['unread_count'] = unread_count
        context['notifications'] = notifications
        context['user'] = user
        return context

@plugin_pool.register_plugin
class PerformanceAnalyticsPluginPublisher(CMSPluginBase):
    model = PerformanceAnalyticsPlugin
    name = _("Performance Analytics Plugin")
    render_template = "performance_analytics_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'default_time_range',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/performance_analytics.css'),
            )
        }
        js = (
            static('js/chart.min.js'),  # Chart.js library
            static('js/performance_analytics.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # Get the current user from the request
        request = context['request']
        user = request.user
        
        # Get chart data
        chart_data = instance.get_chart_data(user)
        
        context['chart_data'] = chart_data
        context['default_time_range'] = instance.default_time_range
        return context


@plugin_pool.register_plugin
class AttendanceTrackerPluginPublisher(CMSPluginBase):
    model = AttendanceTrackerPlugin
    name = _("Attendance Tracker Plugin")
    render_template = "attendance_tracker_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'course',
                'date',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/attendance_tracker.css'),
                static('css/loading_spinner.css'),
            )
        }
        js = (
            static('js/attendance_tracker.js'),
            static('js/loading_spinner.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # We're loading attendance data via AJAX, so we don't need to pass it in the context
        return context

@plugin_pool.register_plugin  # Add our new plugin publisher
class StudyRecommendationPluginPublisher(CMSPluginBase):
    model = StudyRecommendationPlugin
    name = _("Study Recommendation Plugin")
    render_template = "study_recommendation_plugin.html"
    cache = False
    
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'number_of_recommendations',
            )
        }),
    )
    
    class Media:
        css = {
            'all': (
                static('css/study_recommendation.css'),
                static('css/loading_spinner.css'),
            )
        }
        js = (
            static('js/study_recommendation.js'),
            static('js/loading_spinner.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # We're loading recommendations via AJAX, so we don't need to pass them in the context
        return context
