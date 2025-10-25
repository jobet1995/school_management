from typing import TYPE_CHECKING
from django.db import models
from cms.models.pluginmodel import CMSPlugin

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from cms_plugins.models import Announcement
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

class HeroBannerPlugin(CMSPlugin):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='hero_banners/')
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.URLField(blank=True)
    width: int = models.PositiveIntegerField(default=1200, help_text="Width in pixels")  # type: ignore
    height: int = models.PositiveIntegerField(default=400, help_text="Height in pixels")  # type: ignore
    # Custom styling options
    background_color = models.CharField(max_length=7, default="#ffffff", help_text="Background color in hex format (e.g., #ffffff)")
    text_color = models.CharField(max_length=7, default="#000000", help_text="Text color in hex format (e.g., #000000)")
    font_size: int = models.PositiveIntegerField(default=16, help_text="Font size in pixels")  # type: ignore
    
    def __str__(self) -> str:
        return str(self.title)

class FeaturedAnnouncementsPlugin(CMSPlugin):
    title = models.CharField(max_length=200, default="Latest Announcements")  # type: ignore
    number_of_items: int = models.PositiveIntegerField(default=3)  # type: ignore
    
    def get_announcements(self):
        # Import Announcement here to avoid circular import issues
        from cms_plugins.models import Announcement
        return Announcement.objects.filter(is_published=True).order_by('-created_at')[:self.number_of_items]
    
    def __str__(self) -> str:
        return str(self.title)