from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.contrib import admin

from .models import HeroBannerPlugin, FeaturedAnnouncementsPlugin, UpcomingEventsPlugin, WelcomeSectionPlugin, QuickLinksPlugin, QuickLinkItem, StatisticsCounterPlugin, StatisticsCounterItem, TestimonialPlugin, TestimonialItem, CTABannerPlugin


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
            'all': (static('css/admin/cms_plugins_admin.css'),)
        }

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
            'all': (static('css/featured_announcements.css'),)
        }
        js = (
            static('js/featured_announcements.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['announcements'] = instance.get_announcements()
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
    )
    
    class Media:
        css = {
            'all': (static('css/upcoming_events.css'),)
        }
        js = (
            static('js/upcoming_events.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['events'] = instance.get_events()
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
            'all': (static('css/welcome_section.css'),)
        }
        js = (
            static('js/welcome_section.js'),
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
            'all': (static('css/quick_links.css'),)
        }
        js = (
            static('js/quick_links.js'),
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
            'all': (static('css/statistics_counter.css'),)
        }
        js = (
            static('js/statistics_counter.js'),
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
            'all': (static('css/testimonial.css'),)
        }
        js = (
            static('js/testimonial.js'),
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
            'all': (static('css/cta_banner.css'),)
        }
        js = (
            static('js/cta_banner.js'),
        )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context