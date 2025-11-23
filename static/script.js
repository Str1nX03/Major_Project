// ===================================
// CYBERPUNK AI LEARNING PLATFORM
// Interactive JavaScript
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    // ===================================
    // PARTICLE GENERATOR
    // ===================================
    function createParticles() {
        // Skip particle creation if user prefers reduced motion
        if (prefersReducedMotion) return;
        
        const particlesContainer = document.querySelector('.particles');
        if (!particlesContainer) return;
        
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.width = (Math.random() * 3 + 1) + 'px';
            particle.style.height = particle.style.width;
            particle.style.animationDelay = Math.random() * 10 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particlesContainer.appendChild(particle);
        }
    }
    
    createParticles();
    
    // ===================================
    // SCROLL ANIMATIONS
    // ===================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
    
    // ===================================
    // FLASH MESSAGES AUTO-DISMISS
    // ===================================
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.4s ease-out';
            setTimeout(() => message.remove(), 400);
        }, 5000);
    });
    
    // ===================================
    // DASHBOARD FORM SUBMISSION
    // ===================================
    const dashboardForm = document.getElementById('course-form');
    if (dashboardForm) {
        dashboardForm.addEventListener('submit', function(e) {
            const submitBtn = dashboardForm.querySelector('button[type="submit"]');
            const loadingContainer = document.querySelector('.loading-container');
            const formCard = document.querySelector('.dashboard-form .glass-card');
            
            if (submitBtn && loadingContainer) {
                submitBtn.style.display = 'none';
                loadingContainer.classList.add('active');
                
                // Animate progress bar
                const progressFill = loadingContainer.querySelector('.progress-fill');
                if (progressFill) {
                    setTimeout(() => {
                        progressFill.style.width = '100%';
                    }, 100);
                }
                
                // Hide form card after submission
                if (formCard) {
                    setTimeout(() => {
                        formCard.style.opacity = '0.5';
                    }, 300);
                }
            }
        });
    }
    
    // ===================================
    // LESSON ACCORDION
    // ===================================
    const lessonHeaders = document.querySelectorAll('.lesson-header');
    lessonHeaders.forEach((header, index) => {
        header.style.setProperty('--index', index);
        
        header.addEventListener('click', function() {
            const lessonCard = this.parentElement;
            const isActive = lessonCard.classList.contains('active');
            
            // Close all lessons
            document.querySelectorAll('.lesson-card').forEach(card => {
                card.classList.remove('active');
            });
            
            // Open clicked lesson if it wasn't active
            if (!isActive) {
                lessonCard.classList.add('active');
                
                // Smooth scroll to lesson
                setTimeout(() => {
                    lessonCard.scrollIntoView({
                        behavior: 'smooth',
                        block: 'nearest'
                    });
                }, 100);
            }
        });
    });
    
    // Set animation delay for lesson cards
    document.querySelectorAll('.lesson-card').forEach((card, index) => {
        card.style.setProperty('--index', index);
    });
    
    // ===================================
    // BUTTON RIPPLE EFFECT
    // ===================================
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // ===================================
    // TYPING ANIMATION FOR WELCOME TEXT
    // ===================================
    const welcomeText = document.querySelector('.welcome-text');
    if (welcomeText) {
        const originalText = welcomeText.textContent;
        welcomeText.textContent = '';
        let charIndex = 0;
        
        function typeChar() {
            if (charIndex < originalText.length) {
                welcomeText.textContent += originalText.charAt(charIndex);
                charIndex++;
                setTimeout(typeChar, 50);
            }
        }
        
        setTimeout(typeChar, 500);
    }
    
    // ===================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ===================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
    
    // ===================================
    // FORM INPUT ANIMATIONS
    // ===================================
    const formInputs = document.querySelectorAll('.form-input');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Add focused class if input has value on page load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
    
    // ===================================
    // PARALLAX EFFECT ON HERO SECTION
    // ===================================
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && !prefersReducedMotion) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = heroSection.querySelector('.hero-content');
            if (parallax && scrolled < window.innerHeight) {
                parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
                parallax.style.opacity = 1 - (scrolled / window.innerHeight);
            }
        });
    }
    
    // ===================================
    // FEATURE CARD TILT EFFECT
    // ===================================
    const featureCards = document.querySelectorAll('.feature-card');
    if (!prefersReducedMotion) {
        featureCards.forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
            });
        });
    }
    
    // ===================================
    // STUDY LINK HOVER EFFECT
    // ===================================
    const studyLinks = document.querySelectorAll('.study-link');
    studyLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.animation = 'none';
            setTimeout(() => {
                this.style.animation = 'linkBounce 0.5s ease-out';
            }, 10);
        });
    });
    
    // ===================================
    // LOADING SCREEN TIMEOUT WARNING
    // ===================================
    const loadingContainer = document.querySelector('.loading-container.active');
    if (loadingContainer) {
        setTimeout(() => {
            const loadingText = loadingContainer.querySelector('.loading-text');
            if (loadingText) {
                loadingText.innerHTML += '<br><small>Still processing... Thanks for your patience!</small>';
            }
        }, 30000); // After 30 seconds
    }
    
    // ===================================
    // AUTO-EXPAND FIRST LESSON
    // ===================================
    const firstLesson = document.querySelector('.lesson-card');
    if (firstLesson && document.querySelectorAll('.lesson-card').length > 0) {
        setTimeout(() => {
            firstLesson.classList.add('active');
        }, 800);
    }
    
    // ===================================
    // CONSOLE EASTER EGG
    // ===================================
    console.log('%c🚀 Welcome to the Cyberpunk AI Learning Platform!', 'color: #8A2BE2; font-size: 20px; font-weight: bold;');
    console.log('%cBuilt with ❤️ and AI', 'color: #2979FF; font-size: 14px;');
    
});

// ===================================
// ADDITIONAL ANIMATIONS CSS
// ===================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes linkBounce {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(2deg); }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        pointer-events: none;
        animation: rippleEffect 0.6s ease-out;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
