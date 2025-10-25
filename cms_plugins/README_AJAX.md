# Featured Announcements Plugin - AJAX Implementation

This document describes the AJAX implementation for the FeaturedAnnouncementsPlugin in Django CMS.

## Overview

The FeaturedAnnouncementsPlugin now loads announcements dynamically via AJAX instead of server-side rendering. This improves page load performance and provides a better user experience.

## Implementation Details

### 1. Backend (Django)

- **View**: `FeaturedAnnouncementsAjaxView` in `cms_plugins/views.py`
  - Handles AJAX requests for announcements data
  - Returns JSON response with announcements data
  - Includes CSRF protection

- **URL**: `/cms-plugins/featured-announcements/<plugin_id>/`
  - Endpoint for AJAX requests
  - Returns announcements for a specific plugin instance

- **Model Method**: `get_announcements_data()` in `FeaturedAnnouncementsPlugin`
  - Returns announcements data in JSON-serializable format
  - Includes title, content, date, and featured status

### 2. Frontend (JavaScript)

- **File**: `cms_plugins/static/js/featured_announcements.js`
  - Fetches announcements via AJAX on page load
  - Dynamically populates the announcements container
  - Implements fade-in animations for each announcement
  - Handles error cases with user-friendly messages
  - Maintains carousel functionality if enabled

### 3. Template

- **File**: `cms_plugins/templates/featured_announcements_plugin.html`
  - Simplified template with loading state
  - No server-side announcements rendering
  - Data attributes for JavaScript integration

## Usage

### 1. Create Sample Announcements

Run the management command to create sample announcements for testing:

```bash
python manage.py create_sample_announcements
```

### 2. Add Plugin to Page

1. In Django Admin, create a new page or edit an existing one
2. Add the "Featured Announcements Plugin" to a placeholder
3. Configure the plugin settings:
   - Title
   - Number of items to display
   - Enable carousel (optional)

### 3. View in Browser

When the page loads, the announcements will be fetched via AJAX and displayed with fade-in animations.

## Features

- **AJAX Loading**: Announcements are loaded dynamically without page refresh
- **Fade-in Animations**: Each announcement fades in with a staggered delay
- **Error Handling**: User-friendly error messages if announcements fail to load
- **CSRF Protection**: Secure AJAX requests with CSRF token handling
- **Responsive Design**: Works on all device sizes
- **Carousel Support**: Maintains carousel functionality when enabled

## Error Handling

The implementation includes comprehensive error handling:

1. **Network Errors**: Displays error message if AJAX request fails
2. **Server Errors**: Shows error message if server returns an error
3. **Loading State**: Shows loading indicator while fetching data
4. **Empty State**: Handles case when no announcements are available

## Customization

### CSS Classes

- `.featured-announcements`: Main container
- `.announcements-list`: Container for announcement items
- `.announcement-item`: Individual announcement
- `.announcement-item.featured`: Featured announcement styling
- `.announcement-item.fade-in`: Animation class
- `.loading`: Loading state
- `.error`: Error state

### JavaScript Functions

- `fetchAnnouncements()`: Main AJAX function
- `createAnnouncementElement()`: Creates DOM elements for announcements
- `initCarousel()`: Initializes carousel functionality
- `initReadMore()`: Implements read more functionality
- `getCookie()`: Helper function for CSRF token

## Testing

To test the AJAX functionality:

1. Ensure announcements exist in the database
2. Add the plugin to a Django CMS page
3. View the page in a browser
4. Check browser console for any JavaScript errors
5. Verify announcements load correctly with animations

## Troubleshooting

### Common Issues

1. **Announcements not loading**:
   - Check browser console for JavaScript errors
   - Verify CSRF token is being sent correctly
   - Ensure the plugin ID is correct in the data attribute

2. **Animations not working**:
   - Check CSS classes are applied correctly
   - Verify JavaScript is loaded without errors

3. **Carousel not functioning**:
   - Ensure carousel is enabled in plugin settings
   - Check JavaScript console for errors

### Debugging Tips

1. Use browser developer tools to inspect network requests
2. Check Django server logs for any errors
3. Verify the AJAX endpoint returns correct JSON data
4. Test the endpoint directly in the browser