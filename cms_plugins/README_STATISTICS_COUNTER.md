# Statistics Counter Plugin

This plugin provides animated statistics counters for Django CMS with jQuery-based animations that trigger when counters scroll into view.

## Features

- **Scroll-Triggered Animations**: Numbers animate from 0 to their target value when scrolled into view
- **One-Time Animation**: Animation runs only once per page load for optimal performance
- **Optional Icons**: Support for Font Awesome or other icon libraries next to each counter
- **Responsive Design**: Grid layout that adapts to different screen sizes (desktop, tablet, mobile)
- **Smooth Animations**: Customizable animation duration with smooth incrementing
- **Error Handling**: Graceful handling of edge cases and errors

## Components

### 1. StatisticsCounterPlugin Model
Located in `models.py`, the main plugin model that contains multiple counter items.

### 2. StatisticsCounterItem Model
Located in `models.py`, represents individual counters with:
- `label`: Display text for the counter
- `value`: Numeric value to animate to
- `icon`: Optional icon class (e.g., "fa fa-users")

### 3. CMS Plugin Registration
Registered in `cms_plugins.py` with inline admin interface for managing counter items.

### 4. Frontend Implementation
jQuery/JavaScript features in `statistics_counter.js`:
- Scroll detection using Intersection Observer API
- Animated number incrementing with smooth transitions
- One-time execution per counter
- Responsive grid layout

## Usage

### 1. Add to Django CMS Page
1. Edit a page in Django CMS
2. Add the "Statistics Counter Plugin" from the plugin menu
3. Add counter items using the inline admin interface
4. Configure labels, values, and optional icons
5. Save and publish the page

### 2. Direct URL Access
Demo page available at: `/cms_plugins/statistics-counter-demo/`

### 3. Sample Data
Populate the database with sample counters:
```bash
python manage.py create_sample_statistics
```

## Testing

Test the functionality:
```bash
python manage.py test_statistics_counter
```

## Files

- `models.py`: StatisticsCounterPlugin and StatisticsCounterItem models
- `cms_plugins.py`: CMS plugin registration
- `views.py`: Demo view for testing
- `urls.py`: URL patterns
- `templates/statistics_counter_plugin.html`: Plugin template
- `templates/statistics_counter_demo.html`: Standalone demo template
- `static/css/statistics_counter.css`: Responsive styling
- `static/js/statistics_counter.js`: jQuery animation implementation
- `management/commands/create_sample_statistics.py`: Sample data command
- `management/commands/test_statistics_counter.py`: Test command

## Implementation Details

### jQuery Animation
The animation uses jQuery with django.jQuery to ensure compatibility with Django CMS:
- Debounced scroll detection using Intersection Observer
- Smooth number incrementing with requestAnimationFrame-like behavior
- 2-second animation duration by default
- Locale-aware number formatting with thousands separators

### Responsive Design
CSS Grid layout with responsive breakpoints:
- Desktop: Multiple columns in a grid
- Tablet: Reduced gap and padding
- Mobile: Single column layout with centered items

### Performance Optimization
- Animation triggers only once per page load
- Efficient DOM querying with jQuery
- Minimal reflows and repaints
- Cleanup of observer after execution

## Customization

### Styling
Modify `static/css/statistics_counter.css` to customize:
- Colors, fonts, and spacing
- Hover effects and transitions
- Responsive breakpoints
- Icon sizes and positioning

### Animation
Modify `static/js/statistics_counter.js` to customize:
- Animation duration
- Easing functions
- Start delay
- Formatting options

### Content
Use the Django admin interface to customize:
- Counter labels and values
- Icons and their positioning
- Number of counters displayed