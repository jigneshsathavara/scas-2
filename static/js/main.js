document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Configuration
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    let currentTheme = localStorage.getItem('theme');
    if (!currentTheme) {
        currentTheme = 'dark';
        localStorage.setItem('theme', 'dark');
    }
    
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
            if (document.querySelector('canvas:not(#ambient-canvas)')) {
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

    // 3. Responsive Menu Drawer Controls
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.add('open');
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
    }

    if (sidebar) {
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && (!sidebarToggle || !sidebarToggle.contains(e.target))) {
                sidebar.classList.remove('open');
            }
        });
    }

    // 4. Metric Value Count-Up Animation
    const metricValues = document.querySelectorAll('.metric-card .value');
    metricValues.forEach(val => {
        const text = val.textContent.trim();
        const match = text.match(/^([^\d]*)([\d,.]+)([^\d]*)$/);
        if (match) {
            const prefix = match[1];
            const numberStr = match[2].replace(/,/g, '');
            const suffix = match[3];
            const targetNum = parseFloat(numberStr);
            
            if (!isNaN(targetNum) && targetNum > 0) {
                const duration = 1200; // 1.2 second animation
                const startTime = performance.now();
                const isFloat = numberStr.includes('.');
                const numDecimals = isFloat ? numberStr.split('.')[1].length : 0;
                
                const animateCount = (now) => {
                    const progress = Math.min((now - startTime) / duration, 1);
                    // Ease out quadratic
                    const easeProgress = progress * (2 - progress);
                    const currentNum = targetNum * easeProgress;
                    
                    let formattedNum = currentNum.toFixed(numDecimals);
                    if (!isFloat && targetNum > 1000) {
                        formattedNum = Math.floor(currentNum).toLocaleString();
                    }
                    
                    val.textContent = `${prefix}${formattedNum}${suffix}`;
                    
                    if (progress < 1) {
                        requestAnimationFrame(animateCount);
                    } else {
                        val.textContent = text; // safety fallback to exact design string
                    }
                };
                requestAnimationFrame(animateCount);
            }
        }
    });

    // 5. Spotlight Glow cursor position tracking
    document.addEventListener('mousemove', (e) => {
        const cards = document.querySelectorAll('.metric-card, .panel, .login-card');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // 6. Interactive Ambient Canvas Starfield
    const canvas = document.getElementById('ambient-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = (canvas.width = window.innerWidth);
        let height = (canvas.height = window.innerHeight);

        window.addEventListener('resize', () => {
            width = (canvas.width = window.innerWidth);
            height = (canvas.height = window.innerHeight);
        });

        const particles = [];
        const numParticles = 65;
        const mouse = { x: null, y: null, radius: 120 };

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('mouseleave', () => {
            mouse.x = null;
            mouse.y = null;
        });

        class Particle {
            constructor() {
                this.reset();
            }

            reset() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = Math.random() * 0.4 - 0.2;
                this.speedY = Math.random() * 0.4 - 0.2;
                this.alpha = Math.random() * 0.5 + 0.15;
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                // Repulsion force from cursor position
                if (mouse.x !== null && mouse.y !== null) {
                    const dx = this.x - mouse.x;
                    const dy = this.y - mouse.y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < mouse.radius) {
                        const force = (mouse.radius - dist) / mouse.radius;
                        const angle = Math.atan2(dy, dx);
                        this.x += Math.cos(angle) * force * 1.8;
                        this.y += Math.sin(angle) * force * 1.8;
                    }
                }

                // Warp/Wrap bounds
                if (this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
                    this.reset();
                }
            }

            draw() {
                ctx.save();
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                const activeTheme = document.documentElement.getAttribute('data-theme');
                const isDark = activeTheme === 'dark';
                
                ctx.fillStyle = isDark ? `rgba(139, 92, 246, ${this.alpha})` : `rgba(79, 70, 229, ${this.alpha * 0.55})`;
                ctx.shadowBlur = this.size * 2.5;
                ctx.shadowColor = isDark ? '#8b5cf6' : '#4f46e5';
                ctx.fill();
                ctx.restore();
            }
        }

        for (let i = 0; i < numParticles; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        
        animate();
    }
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
