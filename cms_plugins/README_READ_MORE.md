# Read More Functionality for FeaturedAnnouncementsPlugin

This enhancement adds AJAX-based "Read More" functionality to the FeaturedAnnouncementsPlugin, allowing users to expand announcement content without page refresh.

## Features

- **AJAX Content Loading**: Fetches full announcement content via AJAX when "Read More" is clicked
- **Slide Animations**: Smooth slide-down expansion and slide-up collapse animations
- **Toggle Functionality**: Switches between "Read More" and "Show Less" states
- **CSRF Protection**: Secure AJAX requests with proper CSRF token handling
- **Inline Expansion**: Expands content directly within the announcement item
- **Responsive Design**: Works across all device sizes

## Components

### 1. FeaturedAnnouncementDetailView
A new Django view that serves full announcement content via AJAX:
- Located in `views.py`
- Returns JSON response with complete announcement data
- Includes proper error handling

### 2. URL Endpoint
New URL pattern for fetching announcement details:
- `/cms_plugins/featured-announcements/detail/<int:announcement_id>/`

### 3. JavaScript Implementation
Enhanced `featured_announcements.js` with:
- AJAX-based content fetching
- Slide animations for content expansion/collapse
- Dynamic button text switching
- CSRF token integration

### 4. CSS Styling
Updated `featured_announcements.css` with:
- Smooth transition effects
- Overflow handling for animated content
- Responsive design considerations

## Implementation Details

### AJAX Workflow
1. User clicks "Read More" button
2. JavaScript captures announcement ID
3. AJAX request sent to detail view with CSRF protection
4. Server returns full content in JSON format
5. Content expanded with slide-down animation
6. Button text changes to "Show Less"
7. Clicking "Show Less" collapses content with slide-up animation

### Animation Mechanics
- Uses CSS transitions for smooth height animations
- Calculates natural content height for proper expansion
- Maintains content flow during animation
- Preserves scroll position during expansion

### Security
- CSRF token included in all AJAX requests
- Proper error handling for failed requests
- Server-side validation of announcement IDs
- Protection against unauthorized content access

## Usage

### 1. Content Requirements
Announcements must have content longer than 200 characters to trigger the "Read More" button.

### 2. Automatic Integration
The functionality is automatically enabled for all FeaturedAnnouncementsPlugin instances.

### 3. Sample Data
Populate the database with long announcements for testing:
```bash
python manage.py create_sample_long_announcements
```

## Files

- `views.py`: FeaturedAnnouncementDetailView implementation
- `urls.py`: URL pattern for detail endpoint
- `static/js/featured_announcements.js`: Enhanced JavaScript with AJAX functionality
- `static/css/featured_announcements.css`: Updated CSS for animations
- `management/commands/create_sample_long_announcements.py`: Sample data command

## Customization

### Animation Duration
Modify transition duration in CSS:
```css
.announcement-content {
    transition: max-height 0.3s ease;
}
```

### Content Truncation
Adjust truncation length in JavaScript:
```javascript
// In createAnnouncementElement function
const content = announcement.content.length > 200 ? 
    announcement.content.substring(0, 200) + '...' : 
    announcement.content;
```

### Styling
Customize button appearance in CSS:
```css
.read-more-btn {
    /* Custom styles */
}
```

## Testing

Test the functionality by:
1. Creating announcements with long content
2. Viewing the FeaturedAnnouncementsPlugin on a page
3. Clicking "Read More" buttons
4. Verifying AJAX content loading and animations
5. Testing "Show Less" functionality