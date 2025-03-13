/**
 * Main JavaScript for Fridge Monitor System
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enable all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert.alert-success, .alert.alert-info');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Format any temperature inputs to one decimal place
    const tempInputs = document.querySelectorAll('input[type="number"][step="0.1"]');
    tempInputs.forEach(input => {
        input.addEventListener('change', function() {
            this.value = parseFloat(this.value).toFixed(1);
        });
    });
});

/**
 * Format a timestamp for display
 * @param {string} timestamp - ISO timestamp string
 * @param {boolean} includeDate - Whether to include the date
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp, includeDate = false) {
    const date = new Date(timestamp);
    
    if (includeDate) {
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } else {
        return date.toLocaleTimeString();
    }
}

/**
 * Format a duration in seconds to a human-readable format
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds} sec`;
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes} min ${remainingSeconds} sec`;
    } else {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours} hr ${minutes} min`;
    }
}

/**
 * Update an element with new text content and an optional CSS class
 * @param {string} selector - CSS selector for the element
 * @param {string} text - New text content
 * @param {string|null} addClass - CSS class to add (optional)
 * @param {string|null} removeClass - CSS class to remove (optional)
 */
function updateElement(selector, text, addClass = null, removeClass = null) {
    const element = document.querySelector(selector);
    if (element) {
        element.textContent = text;
        
        if (addClass) {
            element.classList.add(addClass);
        }
        
        if (removeClass) {
            element.classList.remove(removeClass);
        }
    }
}
