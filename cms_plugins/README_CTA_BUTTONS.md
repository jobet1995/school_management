# CTA Button Functionality for CTABannerPlugin

This enhancement adds advanced functionality to CTA buttons in the CTABannerPlugin, including smooth scrolling, hover effects, and responsive behavior.

## Features

- **Smooth Scrolling**: Animated scrolling to target sections with duration based on distance
- **Sticky Navbar Offset**: Automatic offset calculation for sticky navigation bars
- **Hover Effects**: Scale-up animation on button hover
- **Responsive Design**: Works across all device sizes
- **Dynamic Duration**: Scroll animation duration adjusts based on distance (500-1500ms)

## Components

### 1. JavaScript Implementation
Enhanced `cta_banner.js` with:
- Smooth scroll-to functionality for anchor links
- Dynamic scroll duration calculation
- Sticky navbar offset handling
- Hover effect animations
- jQuery-based implementation with django.jQuery compatibility

### 2. CSS Styling
Updated `cta_banner.css` with:
- CSS transition effects for hover animations
- Scale transform on hover
- Responsive design considerations
- Shadow effects for depth

### 3. Template Structure
Enhanced `cta_banner_plugin.html` with:
- Proper anchor link handling
- Semantic HTML structure
- Data attributes for JavaScript interaction

## Implementation Details

### Smooth Scrolling
1. **Anchor Link Detection**: Identifies CTA buttons with hash (#) links
2. **Target Element**: Locates target section by ID
3. **Offset Calculation**: Accounts for sticky navbar height
4. **Distance-Based Duration**: Calculates animation duration based on scroll distance
5. **jQuery Animation**: Uses jQuery's animate() method for smooth scrolling

### Hover Effects
1. **CSS Transitions**: Uses CSS for smooth transform animations
2. **Scale Transformation**: Scales button to 1.05 on hover
3. **Shadow Effects**: Adds drop shadow for depth perception
4. **Color Transition**: Changes background/foreground colors on hover

### Offset Handling
1. **Navbar Detection**: Automatically detects navbar height
2. **Dynamic Calculation**: Adjusts scroll position based on navbar height
3. **Fallback Support**: Uses 0px offset if navbar not found

### Responsive Behavior
- Works on all screen sizes
- Maintains proper spacing and sizing
- Preserves animation quality on mobile devices

## Usage

### 1. Content Requirements
- Create CTA banners through Django admin interface
- Set CTA link to internal anchor (e.g., #section-id)
- Ensure target sections have corresponding IDs

### 2. Automatic Integration
The functionality is automatically enabled for all CTABannerPlugin instances.

### 3. Demo Page
Test the functionality with the demo page:
```bash
# Access at: /cms_plugins/cta-banner-demo/
```

## Files

- `static/js/cta_banner.js`: Enhanced JavaScript with scroll and hover functionality
- `static/css/cta_banner.css`: Updated CSS for hover effects and transitions
- `templates/cta_banner_plugin.html`: Template with proper anchor links
- `templates/cta_banner_demo.html`: Demo page for testing
- `views.py`: Demo view implementation
- `urls.py`: URL pattern for demo page

## Customization

### Scroll Duration
Modify duration calculation in JavaScript:
```javascript
const duration = Math.min(1500, Math.max(500, distance / 3)); // Between 500-1500ms
```

### Hover Effect
Adjust hover animation in CSS:
```css
.cta-button:hover {
    transform: scale(1.05); /* Adjust scale factor */
}
```

### Navbar Offset
Customize navbar selector in JavaScript:
```javascript
const navbarHeight = $('.navbar').outerHeight() || 0; // Change selector as needed
```

### Animation Timing
Modify transition duration in CSS:
```css
.cta-button {
    transition: all 0.3s ease; /* Adjust timing */
}
```

## Testing

Test the functionality by:
1. Creating a CTA banner with anchor links
2. Adding target sections with corresponding IDs
3. Verifying smooth scroll behavior
4. Testing hover effects
5. Checking navbar offset calculation
6. Confirming responsive behavior

## Accessibility

- Proper focus states for keyboard navigation
- Sufficient color contrast
- Semantic HTML structure
- Preserved browser default behaviors