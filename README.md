# Django template for a new django CMS 4 project

A Django template for a typical django CMS installation with no 
special bells or whistles. It is supposed as a starting point 
for new projects.

If you prefer a different set of template settings, feel free to 
create your own templates by cloning this repo.

To install django CMS 4 by hand type the following commands:

1. Create virtual environment and activate it
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install Django, django CMS and other required packages
   ```
   pip install django-cms
   ```
3. Create project `<<project_name>>` using this template
   ```
   djangocms <<project_name>>
   cd <<project_name>>
   ```
4. Run testserver
   ```
   ./manage.py runserver
   ```

Note: If you run into a problem of missing dependencies, please
update `pip` using `pip install -U pip` before running the 
`djangocms` command.

## Additional Features

This project includes several custom plugins and features:

### Course Search Plugin
A dynamic course search functionality with AJAX, debounce, and smooth animations.
- Real-time search as users type
- Multi-field search across title, code, description, and instructor
- Responsive grid layout for results
- Loading states and error handling
- See `cms_plugins/README_COURSE_SEARCH.md` for detailed documentation

### Statistics Counter Plugin
Animated statistics counters that increment when scrolled into view.
- Scroll-triggered animations with jQuery
- One-time execution per page load
- Optional icons support
- Fully responsive design
- See `cms_plugins/README_STATISTICS_COUNTER.md` for detailed documentation

### Featured Announcements Plugin
Enhanced announcements with AJAX-based "Read More" functionality.
- Expandable content without page refresh
- Smooth slide animations for content expansion
- CSRF-protected AJAX requests
- Toggle between "Read More" and "Show Less"
- See `cms_plugins/README_READ_MORE.md` for detailed documentation

### Testimonial Plugin
Enhanced testimonials with carousel functionality.
- Rotating carousel with navigation controls
- Mobile swipe support
- Automatic rotation with hover pause
- Fade animations for content transitions
- Responsive layout for all device sizes
- See `cms_plugins/README_TESTIMONIAL_CAROUSEL.md` for detailed documentation

### CTA Banner Plugin
Enhanced CTA buttons with smooth scrolling and hover effects.
- Smooth scrolling to target sections with dynamic duration
- Automatic offset for sticky navigation bars
- Hover effects with scale-up animations
- Responsive design for all device sizes
- See `cms_plugins/README_CTA_BUTTONS.md` for detailed documentation

### Global Loading Spinner
Automatic loading spinner for all AJAX requests.
- Shows spinner when any AJAX request starts
- Hides spinner when requests complete
- Works with all AJAX-enabled plugins
- Accessible design with ARIA attributes
- See `cms_plugins/README_LOADING_SPINNER.md` for detailed documentation