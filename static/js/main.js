// Main JavaScript file for AGBOT application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any components
    initializeApp();
});

function initializeApp() {
    // Add smooth scrolling
    addSmoothScrolling();

    // Initialize notification badge
    initializeNotifications();

    // Add export functionality
    initializeExportButtons();

    // Initialize floating action button
    initializeFAB();

    // Initialize theme toggle
    initializeThemeToggle();
}

// Smooth scrolling for anchor links
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize notifications
function initializeNotifications() {
    const notificationIcon = document.querySelector('.notifications');
    if (notificationIcon) {
        notificationIcon.addEventListener('click', function() {
            alert('You have 1 new pest detection alert!');
            // In a real app, this would show a dropdown with notifications
        });
    }
}

// Export functionality
function initializeExportButtons() {
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            exportData(this.dataset.export);
        });
    });
}

function exportData(type) {
    // In a real application, this would generate and download a report
    alert(`Exporting ${type} report... This feature will be available soon!`);
}

// Utility function to format dates
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Utility function to show loading state
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// API helper function
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Add image preview functionality
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Floating Action Button
function initializeFAB() {
    const fabButton = document.getElementById('fabButton');
    const fabMenu = document.getElementById('fabMenu');

    if (!fabButton || !fabMenu) return;

    fabButton.addEventListener('click', function(e) {
        e.stopPropagation();
        fabButton.classList.toggle('active');
        fabMenu.classList.toggle('active');
    });

    // Close FAB menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!fabButton.contains(e.target) && !fabMenu.contains(e.target)) {
            fabButton.classList.remove('active');
            fabMenu.classList.remove('active');
        }
    });

    // Close FAB menu when a menu item is clicked (except theme toggle and notifications)
    const fabMenuItems = fabMenu.querySelectorAll('.fab-menu-item:not(.fab-theme-toggle):not(.fab-notifications)');
    fabMenuItems.forEach(item => {
        item.addEventListener('click', function() {
            fabButton.classList.remove('active');
            fabMenu.classList.remove('active');
        });
    });
}

// Theme Toggle
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const fabThemeToggle = document.getElementById('fabThemeToggle');

    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    // Navbar theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleTheme();
        });
    }

    // FAB theme toggle
    if (fabThemeToggle) {
        fabThemeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleTheme();
        });
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    // Update theme in database if user is logged in
    fetch('/api/update_theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme: newTheme })
    }).catch(err => console.log('Theme preference not saved to server'));
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    const fabThemeToggle = document.getElementById('fabThemeToggle');

    // Update navbar theme toggle icon
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        }
    }

    // Update FAB theme toggle icon and text
    if (fabThemeToggle) {
        const icon = fabThemeToggle.querySelector('i');
        const span = fabThemeToggle.querySelector('span');
        if (icon && span) {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                span.textContent = 'Light Mode';
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                span.textContent = 'Dark Mode';
            }
        }
    }
}

// Add toast styles dynamically
const style = document.createElement('style');
style.textContent = `
    .toast {
        position: fixed;
        bottom: 90px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: #333;
        color: white;
        border-radius: 0.5rem;
        transform: translateY(100px);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 3000;
    }

    .toast.show {
        transform: translateY(0);
        opacity: 1;
    }

    .toast-success { background: #16a34a; }
    .toast-error { background: #ef4444; }
    .toast-warning { background: #fbbf24; color: #333; }
    .toast-info { background: #3b82f6; }
`;
document.head.appendChild(style);
