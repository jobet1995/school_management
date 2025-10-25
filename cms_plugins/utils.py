from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import LiveNotification

def send_notification_to_user(user, message, category='system'):
    """
    Create a notification for a user and send it via WebSocket if the user is connected.
    """
    # Create the notification in the database
    notification = LiveNotification.objects.create(
        user=user,
        message=message,
        category=category
    )
    
    # Try to send via WebSocket
    try:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            group_name = f'notifications_{user.id}'
            
            # Prepare notification data
            notification_data = {
                'id': notification.id,
                'message': notification.message,
                'category': notification.get_category_display(),
                'category_key': notification.category,
                'is_read': notification.is_read,
                'timestamp': notification.timestamp.isoformat(),
            }
            
            # Send notification to the user's group
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification_update',
                    'notification_data': notification_data
                }
            )
    except Exception as e:
        # If WebSocket fails, that's okay - the notification is still in the database
        print(f"Failed to send WebSocket notification: {e}")
    
    return notification

def calculate_recommendation_score(student, course, difficulty_filter=''):
    """
    Calculate a recommendation score for a course based on student grades and interests.
    Uses a weighted scoring algorithm.
    
    Args:
        student: Student object or None
        course: Course object
        difficulty_filter: String filter for difficulty level
    
    Returns:
        float: Recommendation score (higher is better)
    """
    score = 0.0
    
    # If no student provided, use a basic scoring system
    if not student:
        # Base score based on course popularity or other factors
        score = 50.0  # Default score
        
        # Adjust for difficulty filter if provided
        if difficulty_filter:
            course_difficulty = _get_course_difficulty(course)
            if course_difficulty.lower() == difficulty_filter.lower():
                score += 20  # Boost for matching difficulty
            else:
                score -= 10  # Penalty for non-matching difficulty
                
        return score
    
    # Get student's grades
    try:
        from .models import Grade, Enrollment
        grades = Grade.objects.filter(student=student)
        
        # Weight factors
        grade_weight = 0.4
        interest_weight = 0.3
        enrollment_weight = 0.2
        category_weight = 0.1
        
        # 1. Grade-based scoring
        # Find grades in the same category as this course
        category_grades = grades.filter(course__category=course.category)
        if category_grades.exists():
            # Calculate average grade in this category
            grade_points = {
                'A+': 4.0, 'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'D-': 0.7,
                'F': 0.0
            }
            
            total_points = 0
            for grade in category_grades:
                total_points += grade_points.get(grade.grade, 0)
            
            avg_grade = total_points / category_grades.count()
            
            # Higher grades in this category = higher recommendation score
            grade_score = avg_grade * 25  # Scale to 100
            score += grade_score * grade_weight
        else:
            # No grades in this category, give neutral score
            score += 15 * grade_weight
        
        # 2. Interest-based scoring (based on currently enrolled courses)
        enrollments = Enrollment.objects.filter(student=student, is_active=True)
        enrolled_categories = [e.course.category for e in enrollments]
        
        if course.category in enrolled_categories:
            # Student is currently enrolled in this category
            score += 20 * interest_weight
        elif category_grades.exists():
            # Student has taken courses in this category before
            score += 15 * interest_weight
        else:
            # No connection to this category
            score += 5 * interest_weight
        
        # 3. Enrollment-based scoring
        if enrollments.filter(course=course).exists():
            # Student is already enrolled in this course
            score -= 30  # Don't recommend courses they're already taking
        else:
            score += 10 * enrollment_weight
        
        # 4. Category popularity scoring
        # Courses in popular categories get a slight boost
        popular_categories = ['technology', 'science', 'business']
        if course.category in popular_categories:
            score += 5 * category_weight
            
        # Adjust for difficulty filter if provided
        if difficulty_filter:
            course_difficulty = _get_course_difficulty(course)
            if course_difficulty.lower() == difficulty_filter.lower():
                score += 15  # Boost for matching difficulty
            else:
                score -= 10  # Penalty for non-matching difficulty
                
    except Exception as e:
        # If any error occurs, return a default score
        print(f"Error calculating recommendation score: {e}")
        score = 30.0
    
    return max(0, score)  # Ensure non-negative score

def _get_course_difficulty(course):
    """
    Determine the difficulty level of a course based on credits.
    """
    if course.credits >= 4:
        return "Advanced"
    elif course.credits >= 3:
        return "Intermediate"
    else:
        return "Beginner"