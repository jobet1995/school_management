from django.contrib import admin
from .models import HeroBannerPlugin

# HeroBannerPlugin is registered as a CMS plugin, not a regular Django admin model
# It will appear in the Django admin automatically when used in CMS pages