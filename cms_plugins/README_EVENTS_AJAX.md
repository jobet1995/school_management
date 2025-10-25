# Upcoming Events Plugin - AJAX Implementation

This document describes the AJAX implementation for the UpcomingEventsPlugin in Django CMS with filtering capabilities.

## Overview

The UpcomingEventsPlugin now loads events dynamically via AJAX instead of server-side rendering. It also includes filtering capabilities that allow users to filter events by category or date without page refresh.

## Implementation Details

### 1. Backend (Django)

- **View**: `UpcomingEventsAjaxView` in `cms_plugins/views.py`
  - Handles AJAX requests for events data with filtering support
  - Returns JSON response with events data
  - Includes CSRF protection
  - Supports category and date filtering

- **URL**: `/cms-plugins/upcoming-events/<plugin_id>/`
  - Endpoint for AJAX requests
  - Returns events for a specific plugin instance
  - Accepts query parameters for filtering:
    - `category`: Filter by event category (academic, sports, cultural, social, administrative)
    - `date_filter`: Filter by date (today, this_week, this_month)

- **Model Updates**: 
  - Added `category` field to `Event` model with predefined choices
  - Added `show_category_filter` and `show_date_filter` fields to `UpcomingEventsPlugin` model
  - Enhanced `get_events()` and `get_events_data()` methods to support filtering
  - Added `EVENT_CATEGORIES` choices for event categories

### 2. Frontend (JavaScript)

- **File**: `cms_plugins/static/js/upcoming_events.js`
  - Fetches events via AJAX on page load
  - Dynamically populates the events container
  - Implements fade-in animations for each event
  - Handles error cases with user-friendly messages
  - Implements filtering functionality with dropdowns
  - Maintains carousel functionality when enabled
  - Includes responsive handling for mobile swipe support

### 3. Template

- **File**: `cms_plugins/templates/upcoming_events_plugin.html`
  - Simplified template with loading state
  - No server-side events rendering
  - Data attributes for JavaScript integration
  - Filter controls (category and date dropdowns)
  - Reset filter button

### 4. Styling

- **File**: `cms_plugins/static/css/upcoming_events.css`
  - Styles for filter controls
  - Loading, error, and empty states
  - Category-specific styling
  - Responsive adjustments for mobile

## Features

- **AJAX Loading**: Events are loaded dynamically without page refresh
- **Filtering**: Filter events by category or date without page reload
- **Fade-in Animations**: Each event fades in with a staggered delay
- **Loading Spinner**: Shows loading state while fetching data
- **Error Handling**: User-friendly error messages if events fail to load
- **CSRF Protection**: Secure AJAX requests with CSRF token handling
- **Responsive Design**: Works on all device sizes
- **Carousel Support**: Maintains carousel functionality when enabled
- **Mobile Swipe Support**: Touch/swipe support for carousel navigation
- **Countdown Timers**: Real-time countdown timers for each event

## Usage

### 1. Create Sample Events

Run the management command to create sample events for testing:

```bash
python manage.py create_sample_events
```

### 2. Add Plugin to Page

1. In Django Admin, create a new page or edit an existing one
2. Add the "Upcoming Events Plugin" to a placeholder
3. Configure the plugin settings:
   - Title
   - Number of items to display
   - Enable carousel (optional)
   - Show category filter
   - Show date filter

### 3. View in Browser

When the page loads, the events will be fetched via AJAX and displayed with fade-in animations. Users can filter events using the dropdown controls.

## Filtering

The plugin supports two types of filtering:

1. **Category Filter**: Filter events by category (Academic, Sports, Cultural, Social, Administrative)
2. **Date Filter**: Filter events by date range (Today, This Week, This Month)

Filters can be used individually or in combination. The "Reset" button clears all filters.

## Error Handling

The implementation includes comprehensive error handling:

1. **Network Errors**: Displays error message if AJAX request fails
2. **Server Errors**: Shows error message if server returns an error
3. **Loading State**: Shows loading indicator while fetching data
4. **Empty State**: Handles case when no events match the filters

## Customization

### CSS Classes

- `.upcoming-events`: Main container
- `.events-filters`: Container for filter controls
- `.filter-category`: Category dropdown
- `.filter-date`: Date dropdown
- `.filter-reset`: Reset button
- `.events-list`: Container for event items
- `.event-item`: Individual event
- `.event-item.fade-in`: Animation class
- `.loading`: Loading state
- `.error`: Error state
- `.no-events`: Empty state

### JavaScript Functions

- `fetchEvents()`: Main AJAX function with filtering
- `createEventElement()`: Creates DOM elements for events
- `initCarousel()`: Initializes carousel functionality
- `initCountdownTimers()`: Initializes countdown timers
- `getCookie()`: Helper function for CSRF token

## Testing

To test the AJAX functionality:

1. Ensure events exist in the database
2. Add the plugin to a Django CMS page
3. View the page in a browser
4. Check browser console for any JavaScript errors
5. Verify events load correctly with animations
6. Test filtering functionality

## Troubleshooting

### Common Issues

1. **Events not loading**:
   - Check browser console for JavaScript errors
   - Verify CSRF token is being sent correctly
   - Ensure the plugin ID is correct in the data attribute

2. **Animations not working**:
   - Check CSS classes are applied correctly
   - Verify JavaScript is loaded without errors

3. **Carousel not functioning**:
   - Ensure carousel is enabled in plugin settings
   - Check JavaScript console for errors

4. **Filters not working**:
   - Verify the filter dropdowns are properly initialized
   - Check network requests for correct parameters

### Debugging Tips

1. Use browser developer tools to inspect network requests
2. Check Django server logs for any errors
3. Verify the AJAX endpoint returns correct JSON data
4. Test the endpoint directly in the browser with query parameters

## Migration

After updating the models, you'll need to create and apply migrations:

```bash
python manage.py makemigrations cms_plugins
python manage.py migrate cms_plugins
```