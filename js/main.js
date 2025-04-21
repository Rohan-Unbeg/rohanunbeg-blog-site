document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    
    if (burger) {
        burger.addEventListener('click', function() {
            nav.classList.toggle('active');
            
            // Animate burger
            burger.querySelector('.line1').classList.toggle('rotate-45');
            burger.querySelector('.line2').classList.toggle('opacity-0');
            burger.querySelector('.line3').classList.toggle('rotate-neg-45');
        });
    }
    
    // Close mobile nav when clicking outside
    document.addEventListener('click', function(event) {
        if (nav && nav.classList.contains('active') && !nav.contains(event.target) && !burger.contains(event.target)) {
            nav.classList.remove('active');
            
            // Reset burger animation
            burger.querySelector('.line1').classList.remove('rotate-45');
            burger.querySelector('.line2').classList.remove('opacity-0');
            burger.querySelector('.line3').classList.remove('rotate-neg-45');
        }
    });
    
    // Sticky header
    const header = document.querySelector('header');
    let lastScrollPosition = 0;
    
    window.addEventListener('scroll', function() {
        const currentScrollPosition = window.scrollY;
        
        if (currentScrollPosition > 100) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
        
        lastScrollPosition = currentScrollPosition;
    });
    
    // Newsletter form submission
    const newsletterForm = document.getElementById('newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            if (email) {
                // In a real application, you would send this to your backend
                // For now, we'll just show a success message
                alert('Thank you for subscribing to my newsletter!');
                emailInput.value = '';
            }
        });
    }
    
    // Add CSS class for animation to burger lines
    if (burger) {
        const burgerLines = burger.querySelectorAll('div');
        burgerLines.forEach(line => {
            line.classList.add('burger-line');
        });
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Close mobile nav if open
                if (nav && nav.classList.contains('active')) {
                    nav.classList.remove('active');
                    
                    burger.querySelector('.line1').classList.remove('rotate-45');
                    burger.querySelector('.line2').classList.remove('opacity-0');
                    burger.querySelector('.line3').classList.remove('rotate-neg-45');
                }
                
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add animation classes to burger menu
    document.head.insertAdjacentHTML('beforeend', `
        <style>
            .burger-line {
                transition: all 0.3s ease;
            }
            .rotate-45 {
                transform: rotate(45deg) translate(5px, 6px);
            }
            .opacity-0 {
                opacity: 0;
            }
            .rotate-neg-45 {
                transform: rotate(-45deg) translate(5px, -6px);
            }
            .header-scrolled {
                background: rgba(248, 249, 250, 0.95);
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            }
        </style>
    `);
}); 