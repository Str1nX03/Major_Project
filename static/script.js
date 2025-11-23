// ===================================
// CYBERPUNK AI LEARNING PLATFORM
// Interactive JavaScript
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    // ===================================
    // CATALOG DATA (Subject -> Topics)
    // ===================================
    const catalogData = {
        "Mathematics": [
            "Calculus", 
            "Matrix", 
            "Multiplication", 
            "Trigonometry", 
            "Mensuration",
            "Algebra",
            "Geometry",
            "Statistics"
        ],
        "Physics": [
            "Kinematics", 
            "Thermodynamics", 
            "Electromagnetism", 
            "Optics", 
            "Quantum Mechanics",
            "Nuclear Physics",
            "Astrophysics"
        ],
        "Chemistry": [
            "Organic Chemistry", 
            "Inorganic Chemistry", 
            "Physical Chemistry", 
            "Nuclear Chemistry", 
            "Analytical Chemistry",
            "Environmental Chemistry"
        ],
        "Biology": [
            "Genetics", 
            "Cell Biology", 
            "Ecology", 
            "Evolution", 
            "Molecular Biology",
            "Immunity",
            "Neuroscience"
        ],
        "Computer Science": [
            "Data Structures", 
            "Algorithms", 
            "Web Development", 
            "Artificial Intelligence", 
            "Database Management",
            "Cybersecurity",
            "Operating Systems",
            "Machine Learning",
            "Cloud Computing"
        ]
    };

    // ===================================
    // PARTICLE GENERATOR
    // ===================================
    function createParticles() {
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
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card').forEach(card => observer.observe(card));
    
    // ===================================
    // FLASH MESSAGES
    // ===================================
    document.querySelectorAll('.flash-message').forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.4s ease-out';
            setTimeout(() => message.remove(), 400);
        }, 5000);
    });
    
    // ===================================
    // FORM SUBMISSION
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
                const progressFill = loadingContainer.querySelector('.progress-fill');
                if (progressFill) setTimeout(() => progressFill.style.width = '100%', 100);
                if (formCard) setTimeout(() => formCard.style.opacity = '0.5', 300);
            }
        });
    }
    
    // ===================================
    // ORIGINAL IDEAS MODAL
    // ===================================
    const ideasBtn = document.getElementById('ideas-btn');
    const ideasModal = document.getElementById('ideas-modal');
    
    if (ideasBtn && ideasModal) {
        ideasBtn.addEventListener('click', () => {
            ideasModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        ideasModal.addEventListener('click', (e) => {
            if (e.target === ideasModal || e.target.classList.contains('close-modal')) {
                ideasModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // ===================================
    // CATALOG BROWSER LOGIC (NEW)
    // ===================================
    const browseBtn = document.getElementById('browse-catalog-btn');
    const catalogModal = document.getElementById('catalog-modal');
    const catalogCloseBtn = document.querySelector('.close-catalog-modal');
    const subjectListContainer = document.getElementById('subject-list');
    const topicListContainer = document.getElementById('topic-list');
    const stepSubject = document.getElementById('catalog-step-subject');
    const stepTopic = document.getElementById('catalog-step-topic');
    const backBtn = document.getElementById('catalog-back-btn');
    const selectedSubjectDisplay = document.querySelector('#selected-subject-display span');
    
    const subjectInput = document.getElementById('subject');
    const topicInput = document.getElementById('topic');

    let currentSubject = null;

    if (browseBtn && catalogModal) {
        
        // Open Modal
        browseBtn.addEventListener('click', () => {
            renderSubjects();
            showStep('subject');
            catalogModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        // Close Modal
        function closeCatalog() {
            catalogModal.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (catalogCloseBtn) catalogCloseBtn.addEventListener('click', closeCatalog);
        catalogModal.addEventListener('click', (e) => {
            if (e.target === catalogModal) closeCatalog();
        });

        // Render Subjects
        function renderSubjects() {
            subjectListContainer.innerHTML = '';
            Object.keys(catalogData).forEach(subject => {
                const btn = document.createElement('div');
                btn.className = 'catalog-item';
                btn.textContent = subject;
                btn.onclick = () => selectSubject(subject);
                subjectListContainer.appendChild(btn);
            });
        }

        // Select Subject & Show Topics
        function selectSubject(subject) {
            currentSubject = subject;
            selectedSubjectDisplay.textContent = subject;
            
            // Render Topics
            topicListContainer.innerHTML = '';
            const topics = catalogData[subject];
            topics.forEach(topic => {
                const btn = document.createElement('div');
                btn.className = 'catalog-item';
                btn.textContent = topic;
                btn.onclick = () => selectTopic(topic);
                topicListContainer.appendChild(btn);
            });

            showStep('topic');
        }

        // Select Topic -> Fill Form & Close
        function selectTopic(topic) {
            subjectInput.value = currentSubject;
            topicInput.value = topic;
            
            // Visual feedback
            subjectInput.parentElement.classList.add('focused');
            topicInput.parentElement.classList.add('focused');
            
            closeCatalog();
        }

        // Navigation
        function showStep(step) {
            if (step === 'subject') {
                stepSubject.classList.remove('hidden');
                stepTopic.classList.add('hidden');
            } else {
                stepSubject.classList.add('hidden');
                stepTopic.classList.remove('hidden');
            }
        }

        if (backBtn) {
            backBtn.addEventListener('click', () => showStep('subject'));
        }
    }
    
    // ===================================
    // LESSON ACCORDION & OTHER UI
    // ===================================
    const lessonHeaders = document.querySelectorAll('.lesson-header');
    lessonHeaders.forEach((header, index) => {
        header.style.setProperty('--index', index);
        header.addEventListener('click', function() {
            const lessonCard = this.parentElement;
            const isActive = lessonCard.classList.contains('active');
            document.querySelectorAll('.lesson-card').forEach(card => card.classList.remove('active'));
            if (!isActive) {
                lessonCard.classList.add('active');
                setTimeout(() => lessonCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
            }
        });
    });

    document.querySelectorAll('.lesson-card').forEach((card, index) => {
        card.style.setProperty('--index', index);
    });

    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    const formInputs = document.querySelectorAll('.form-input');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() { this.parentElement.classList.add('focused'); });
        input.addEventListener('blur', function() { if (!this.value) this.parentElement.classList.remove('focused'); });
        if (input.value) input.parentElement.classList.add('focused');
    });

    console.log('%c🚀 Cyberpunk AI Platform Ready', 'color: #8A2BE2; font-weight: bold;');
});