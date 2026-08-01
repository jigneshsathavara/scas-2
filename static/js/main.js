document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Configuration
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const currentTheme = localStorage.getItem('theme') || 'dark'; // default theme is dark
    
    // Set theme on body
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Re-render chart colors if charts exist
            if (document.querySelector('canvas')) {
                location.reload(); // Quick refresh is the cleanest way to update Chart.js canvas contexts
            }
        });
    }
    
    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        const iconName = theme === 'light' ? 'moon' : 'sun';
        themeToggleBtn.innerHTML = `<i data-lucide="${iconName}"></i>`;
        if (window.lucide) {
            lucide.createIcons();
        }
        themeToggleBtn.title = theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode';
    }
    
    // 2. Toast Alert Animations / Dismissals
    const toasts = document.querySelectorAll('.toast-alert');
    toasts.forEach(toast => {
        // Auto dismiss after 4 seconds
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 4000);
        
        // Manual dismiss on click
        toast.addEventListener('click', () => {
            toast.style.animation = 'slideIn 0.3s ease reverse forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        });
    });
});

// Helper functions for global modals
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}
