// Quiz functionality JavaScript - Enhanced with animations and interactions

// Utility functions with animations
function showElement(id, animation = 'fadeIn') {
    const element = document.getElementById(id);
    element.classList.remove('d-none');
    element.style.animation = `${animation} 0.5s ease-in-out`;
}

function hideElement(id, animation = 'fadeOut') {
    const element = document.getElementById(id);
    element.style.animation = `${animation} 0.3s ease-in-out`;
    setTimeout(() => {
        element.classList.add('d-none');
    }, 300);
}

// Enhanced form interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add loading states and animations
    enhanceFormSubmissions();
    addProgressAnimations();
    enhanceQuizInteractions();
    addTooltipAnimations();
    initializeParticleBackground();
});

function enhanceFormSubmissions() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                // Add loading state
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                
                // Add pulse animation to form
                form.style.animation = 'pulse 0.3s ease-in-out';
            }
        });
    });
}

function addProgressAnimations() {
    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width || bar.getAttribute('data-width');
        if (width) {
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-in-out';
                bar.style.width = width;
            }, 500);
        }
    });
    
    // Add step completion animations
    const steps = document.querySelectorAll('.step-indicator');
    steps.forEach((step, index) => {
        if (step.classList.contains('completed')) {
            setTimeout(() => {
                step.style.animation = 'checkmark 0.6s ease-in-out';
            }, index * 200);
        }
    });
}

function enhanceQuizInteractions() {
    // Add hover effects and selection animations
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(option => {
        option.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';
        });
        
        option.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        option.addEventListener('click', function() {
            // Remove selection from siblings
            const siblings = this.parentElement.querySelectorAll('.quiz-option');
            siblings.forEach(sib => {
                sib.classList.remove('selected');
                sib.style.animation = '';
            });
            
            // Add selection animation
            this.classList.add('selected');
            this.style.animation = 'selectBounce 0.4s ease';
        });
    });
}

function addTooltipAnimations() {
    // Enhanced tooltips with animations
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const tooltipText = element.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    tooltip.style.animation = 'tooltipFadeIn 0.3s ease';
}

function hideTooltip(element) {
    const tooltips = document.querySelectorAll('.custom-tooltip');
    tooltips.forEach(tooltip => {
        tooltip.style.animation = 'tooltipFadeOut 0.2s ease';
        setTimeout(() => tooltip.remove(), 200);
    });
}

function initializeParticleBackground() {
    // Create floating particles for visual appeal
    const container = document.querySelector('.hero-section, .quiz-container');
    if (!container) return;
    
    for (let i = 0; i < 20; i++) {
        createParticle(container);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'floating-particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 10 + 's';
    particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
    
    container.appendChild(particle);
    
    // Remove particle after animation completes
    setTimeout(() => {
        if (particle.parentNode) {
            particle.remove();
        }
    }, 20000);
}

// Quiz-specific enhancements
function animateQuestionTransition() {
    const currentQuestion = document.querySelector('.question-card.active');
    const nextQuestion = document.querySelector('.question-card.next');
    
    if (currentQuestion && nextQuestion) {
        currentQuestion.style.animation = 'slideOutLeft 0.5s ease-in-out';
        setTimeout(() => {
            currentQuestion.classList.remove('active');
            nextQuestion.classList.add('active');
            nextQuestion.style.animation = 'slideInRight 0.5s ease-in-out';
        }, 500);
    }
}

function updateQuizProgress(current, total) {
    const progressBar = document.querySelector('.quiz-progress-bar');
    const progressText = document.querySelector('.progress-text');
    
    if (progressBar) {
        const percentage = (current / total) * 100;
        progressBar.style.width = percentage + '%';
        progressBar.style.transition = 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
    }
    
    if (progressText) {
        progressText.textContent = `Question ${current} of ${total}`;
        progressText.style.animation = 'numberCount 0.5s ease';
    }
}

function celebrateCorrectAnswer() {
    // Create confetti effect for correct answers
    const confetti = document.createElement('div');
    confetti.className = 'confetti-burst';
    document.body.appendChild(confetti);
    
    setTimeout(() => confetti.remove(), 2000);
}

// Smooth scroll enhancements
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'nearest'
    });
}

// Enhanced typing effect for dynamic text
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Loading screen management
function showLoadingScreen(message = 'Loading...') {
    const loading = document.createElement('div');
    loading.className = 'loading-overlay';
    loading.innerHTML = `
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <p class="loading-text">${message}</p>
        </div>
    `;
    document.body.appendChild(loading);
    
    setTimeout(() => {
        loading.style.animation = 'fadeIn 0.3s ease';
    }, 10);
}

function hideLoadingScreen() {
    const loading = document.querySelector('.loading-overlay');
    if (loading) {
        loading.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => loading.remove(), 300);
    }
}
