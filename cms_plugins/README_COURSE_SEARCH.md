# Course Search Plugin

This plugin provides dynamic course search functionality for Django CMS with AJAX, debounce, and smooth animations.

## Features

- **Dynamic Search**: Real-time search as users type
- **Debounced Requests**: 300ms delay to prevent excessive AJAX calls
- **Multi-field Search**: Searches across course title, code, description, and instructor
- **Responsive Design**: Grid layout that adapts to different screen sizes
- **Loading States**: Visual feedback during search operations
- **Animations**: Smooth fade-in effects for search results
- **Error Handling**: Graceful handling of errors and edge cases

## Components

### 1. Course Model
Located in `models.py`, the [Course](file:///d:/Djang-cms/school_management/cms_plugins/models.py#L32-L56) model includes:
- `title`: Course title
- `code`: Unique course code (e.g., "CS101")
- `description`: Detailed course description
- `category`: Course category (Science, Arts, Business, Technology)
- `instructor`: Instructor name
- `credits`: Number of course credits
- `duration`: Course duration information
- `is_published`: Publication status

### 2. AJAX View
The [CourseSearchAjaxView](file:///d:/Djang-cms/school_management/cms_plugins/views.py#L77-L125) in `views.py` handles search requests:
- Accepts `q` parameter for search queries
- Filters published courses by multiple fields using OR logic
- Returns JSON with course data and metadata
- Limits results to 10 courses for performance

### 3. CMS Plugin
The [CourseSearchPlugin](file:///d:/Djang-cms/school_management/cms_plugins/models.py#L369-L376) can be added to Django CMS pages:
- Configurable title and placeholder text
- Reusable across multiple pages

### 4. Frontend Implementation
jQuery/JavaScript features in the template:
- Debounced input handling (300ms)
- AJAX requests to the search endpoint
- Dynamic result rendering
- Loading and empty states
- CSS animations for results

## Usage

### 1. Add to Django CMS Page
1. Edit a page in Django CMS
2. Add the "Course Search Plugin" from the plugin menu
3. Configure the title and placeholder text
4. Save and publish the page

### 2. Direct URL Access
The search endpoint is available at: `/cms_plugins/course-search/?q=query`

### 3. Sample Data
Populate the database with sample courses:
```bash
python manage.py create_sample_courses
```

## Testing

Test the search functionality:
```bash
python manage.py test_course_search
```

## Files

- `models.py`: Course and CourseSearchPlugin models
- `views.py`: CourseSearchAjaxView and demo view
- `urls.py`: URL patterns for search endpoints
- `cms_plugins.py`: CMS plugin registration
- `templates/course_search_plugin.html`: Plugin template
- `templates/course_search.html`: Standalone demo template
- `static/css/course_search.css`: Plugin styling
- `static/js/course_search.js`: Plugin JavaScript
- `management/commands/create_sample_courses.py`: Sample data command
- `management/commands/test_course_search.py`: Test command