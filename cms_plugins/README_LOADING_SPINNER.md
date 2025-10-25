# Global Loading Spinner for AJAX Requests

This enhancement adds a global loading spinner that automatically appears during AJAX requests across the Django CMS Student Management System.

## Features

- **Automatic Display**: Shows spinner when any AJAX request starts
- **Automatic Hide**: Hides spinner when all requests complete
- **Concurrent Request Tracking**: Properly handles multiple simultaneous requests
- **Error Handling**: Hides spinner even when requests fail
- **Accessible Design**: Includes proper ARIA attributes for screen readers
- **Responsive Layout**: Works on all device sizes
- **Plugin Integration**: Works with FeaturedAnnouncementsPlugin, UpcomingEventsPlugin, and Search plugins

## Components

### 1. CSS Styles
`loading_spinner.css` provides:
- Global overlay with semi-transparent background
- Animated spinner with CSS keyframes
- Responsive design for mobile devices
- Plugin-specific loading indicators

### 2. JavaScript Implementation
`loading_spinner.js` provides:
- Global AJAX event handlers (`ajaxStart`, `ajaxStop`, `ajaxComplete`, `ajaxError`)
- Concurrent request tracking
- Accessible ARIA attributes
- Helper functions for plugin-specific loading indicators

### 3. Plugin Integration
All CMS plugins updated to include:
- Loading spinner CSS in media files
- Loading spinner JavaScript in media files

## Implementation Details

### Global AJAX Tracking
1. **Request Counter**: Tracks active AJAX requests
2. **Show on Start**: Displays spinner on first request
3. **Hide on Complete**: Hides spinner when all requests finish
4. **Error Handling**: Ensures spinner hides even on request failures

### Spinner Design
1. **Overlay**: Full-screen semi-transparent background
2. **Spinner**: Animated CSS spinner with border animation
3. **Text**: "Loading..." text below spinner
4. **Centering**: Vertically and horizontally centered
5. **Transitions**: Smooth fade in/out animations

### Accessibility
1. **ARIA Attributes**: Properly hides/shows spinner for screen readers
2. **Focus Management**: Maintains focus during loading states
3. **Contrast**: Sufficient color contrast for visibility
4. **Animation**: Reduced motion support

### Responsive Behavior
- **Desktop**: Standard sizing and positioning
- **Tablet**: Adjusted padding and sizing
- **Mobile**: Compact design with appropriate spacing

## Usage

### Automatic Integration
The loading spinner is automatically enabled for all CMS plugins:
- FeaturedAnnouncementsPlugin
- UpcomingEventsPlugin
- CourseSearchPlugin
- And all other AJAX-enabled plugins

### Manual Usage
For custom AJAX requests, the spinner will automatically appear:
```javascript
$.ajax({
    url: '/some-endpoint/',
    method: 'GET',
    success: function(data) {
        // Spinner automatically hides when complete
    },
    error: function() {
        // Spinner automatically hides even on error
    }
});
```

### Plugin-Specific Loading
Helper functions for plugin-specific loading indicators:
```javascript
// Show plugin-specific loading indicator
showPluginLoading(container);

// Hide plugin-specific loading indicator
hidePluginLoading(container);
```

## Files

- `static/css/loading_spinner.css`: Global spinner styles
- `static/js/loading_spinner.js`: Global spinner JavaScript
- `cms_plugins.py`: Updated plugin registrations
- `templates/loading_spinner_demo.html`: Demo page
- `views.py`: Demo view implementation
- `urls.py`: URL pattern for demo page

## Customization

### Spinner Appearance
Modify spinner styles in CSS:
```css
.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #007bff; /* Change color here */
}
```

### Overlay Color
Adjust overlay transparency:
```css
.loading-overlay {
    background-color: rgba(0, 0, 0, 0.5); /* Change transparency here */
}
```

### Animation Speed
Modify animation duration:
```css
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
/* Add animation-duration property to .spinner */
```

### Text Content
Change loading text:
```javascript
const loadingOverlay = `
    <div id="global-loading-overlay" class="loading-overlay" aria-hidden="true">
        <div class="spinner-container">
            <div class="spinner"></div>
            <div class="spinner-text">Loading...</div> <!-- Change text here -->
        </div>
    </div>
`;
```

## Testing

Test the functionality by:
1. Accessing the demo page at `/cms_plugins/loading-spinner-demo/`
2. Clicking the demo buttons to trigger AJAX requests
3. Verifying the spinner appears and disappears correctly
4. Testing concurrent requests
5. Testing error scenarios
6. Checking responsive behavior on different screen sizes

## Integration with Existing Plugins

All existing AJAX-enabled plugins automatically integrate with the global loading spinner:
- No code changes required in existing plugin JavaScript
- CSS and JS files automatically included via plugin media definitions
- Works with fetch() and jQuery AJAX requests
- Maintains existing plugin functionality

## Performance

- **Lightweight**: Minimal CSS and JavaScript overhead
- **Efficient**: Uses native jQuery AJAX events
- **Non-blocking**: CSS animations don't block UI thread
- **Optimized**: Single global listener for all AJAX events