from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

from .models import HeroBannerPlugin, FeaturedAnnouncementsPlugin


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
                'background_image',
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

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['announcements'] = instance.get_announcements()
        return context