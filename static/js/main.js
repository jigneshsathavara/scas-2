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
        if (theme === 'light') {
            // Light theme active -> Show moon icon to switch to dark
            themeToggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#facc15" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon" style="display: block;"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>`;
            themeToggleBtn.title = 'Switch to Dark Mode';
        } else {
            // Dark theme active -> Show sun icon to switch to light
            themeToggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#facc15" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun" style="display: block;"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>`;
            themeToggleBtn.title = 'Switch to Light Mode';
        }
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
