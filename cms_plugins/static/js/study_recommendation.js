// Study Recommendation Plugin JavaScript
(function($) {
    // Plugin initialization
    $(document).ready(function() {
        // Add any additional initialization code here if needed
        console.log('Study Recommendation Plugin initialized');
    });
    
    // Export functions if needed for global access
    window.StudyRecommendationPlugin = {
        // Add any public methods here
        refreshRecommendations: function(pluginId) {
            // This function could be called externally to refresh recommendations
            $('#subjectFilter-' + pluginId).trigger('change');
        }
    };
})(django.jQuery);