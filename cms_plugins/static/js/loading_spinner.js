(function($) {
    // Global loading spinner functionality
    $(document).ready(function() {
        // Create loading overlay element
        const loadingOverlay = `
            <div id="global-loading-overlay" class="loading-overlay" aria-hidden="true">
                <div class="spinner-container">
                    <div class="spinner"></div>
                    <div class="spinner-text">Loading...</div>
                </div>
            </div>
        `;
        
        // Append to body
        $('body').append(loadingOverlay);
        
        // Store reference to overlay
        const $loadingOverlay = $('#global-loading-overlay');
        
        // Track active AJAX requests
        let activeRequests = 0;
        
        // Show loading overlay
        function showLoadingOverlay() {
            $loadingOverlay.addClass('active');
            $loadingOverlay.attr('aria-hidden', 'false');
        }
        
        // Hide loading overlay
        function hideLoadingOverlay() {
            $loadingOverlay.removeClass('active');
            $loadingOverlay.attr('aria-hidden', 'true');
        }
        
        // AJAX event handlers
        $(document).ajaxStart(function() {
            activeRequests++;
            if (activeRequests === 1) {
                showLoadingOverlay();
            }
        });
        
        $(document).ajaxStop(function() {
            activeRequests = 0;
            hideLoadingOverlay();
        });
        
        $(document).ajaxComplete(function() {
            if (activeRequests > 0) {
                activeRequests--;
            }
            if (activeRequests === 0) {
                hideLoadingOverlay();
            }
        });
        
        $(document).ajaxError(function() {
            if (activeRequests > 0) {
                activeRequests--;
            }
            if (activeRequests === 0) {
                hideLoadingOverlay();
            }
        });
    });
    
    // Helper function to show plugin-specific loading indicator
    window.showPluginLoading = function(container) {
        const $container = $(container);
        $container.html(`
            <div class="plugin-loading">
                <div class="spinner"></div>
                <span>Loading...</span>
            </div>
        `);
    };
    
    // Helper function to hide plugin-specific loading indicator
    window.hidePluginLoading = function(container) {
        const $container = $(container);
        $container.find('.plugin-loading').remove();
    };
    
})(django.jQuery);