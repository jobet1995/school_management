# Testimonial Plugin Carousel

This enhancement adds carousel functionality to the TestimonialPlugin with automatic rotation, navigation controls, and mobile swipe support.

## Features

- **Rotating Carousel**: Display testimonials in a rotating carousel with next/previous arrows
- **Mobile Swipe Support**: Touch/swipe navigation for mobile devices
- **Automatic Rotation**: Auto-rotate every 5 seconds with hover pause
- **Fade Animations**: Smooth fade-in animations for active testimonials
- **Responsive Layout**: Multiple cards on desktop, fewer on tablet, single on mobile
- **Accessibility**: Proper ARIA labels and keyboard navigation support

## Components

### 1. JavaScript Implementation
Enhanced `testimonial.js` with:
- Carousel navigation with previous/next buttons
- Automatic rotation every 5 seconds
- Hover pause functionality
- Mobile touch/swipe support
- Fade animations for content transitions

### 2. CSS Styling
Updated `testimonial.css` with:
- Smooth fade transition effects
- Responsive grid layouts
- Navigation button styling
- Hover and focus states

### 3. Template Structure
Enhanced `testimonial_plugin.html` with:
- Proper semantic HTML structure
- Accessibility attributes
- Data attributes for JavaScript interaction

## Implementation Details

### Carousel Mechanics
1. **Grid Layout**: Uses CSS Grid for responsive multi-column display
2. **Navigation**: Previous/next buttons positioned absolutely
3. **Auto Rotation**: 5-second interval with clearInterval/setInterval
4. **Hover Pause**: Rotation pauses when user hovers over carousel
5. **Swipe Support**: Touch event handlers for mobile navigation

### Animation System
- Fade transitions using CSS opacity transitions
- 0.5-second duration for smooth animations
- Staggered timing for natural movement
- Hardware-accelerated transforms for performance

### Responsive Behavior
- **Desktop (≥992px)**: 3 testimonials per row
- **Tablet (768px-991px)**: 2 testimonials per row
- **Mobile (<768px)**: 1 testimonial per row
- **Small Mobile (<480px)**: Compact padding and smaller navigation

### Touch Support
- Touchstart/touchend event listeners
- Horizontal swipe detection with 50px threshold
- Direction-based navigation (left swipe = next, right swipe = previous)

## Usage

### 1. Content Requirements
- Create testimonials through Django admin interface
- Mark featured testimonials for special styling
- Add photos, names, courses, and testimonial text

### 2. Automatic Integration
The carousel functionality is automatically enabled for all TestimonialPlugin instances.

### 3. Sample Data
Populate the database with sample testimonials for testing:
```bash
python manage.py create_sample_testimonials
```

## Files

- `static/js/testimonial.js`: Enhanced JavaScript with carousel functionality
- `static/css/testimonial.css`: Updated CSS for responsive layouts and animations
- `templates/testimonial_plugin.html`: Template structure
- `management/commands/create_sample_testimonials.py`: Sample data command

## Customization

### Rotation Speed
Modify rotation delay in JavaScript:
```javascript
const rotationDelay = 5000; // 5 seconds
```

### Animation Duration
Adjust fade transition duration in CSS:
```css
.testimonial-item {
    transition: opacity 0.5s ease, transform 0.5s ease;
}
```

### Grid Layout
Customize responsive breakpoints in CSS:
```css
@media (max-width: 992px) {
    .testimonial-slider {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

### Navigation Buttons
Style navigation buttons in CSS:
```css
.testimonial-nav {
    /* Custom styles */
}
```

## Testing

Test the functionality by:
1. Creating multiple testimonials through admin
2. Viewing the TestimonialPlugin on a page
3. Verifying automatic rotation and hover pause
4. Testing navigation buttons
5. Checking mobile swipe functionality
6. Confirming responsive layout changes
7. Verifying fade animations

## Accessibility

- Proper ARIA labels for navigation buttons
- Keyboard navigable controls
- Sufficient color contrast
- Focus states for interactive elements
- Semantic HTML structure