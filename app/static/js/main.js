// Add scroll effect to hub navigation
document.addEventListener('DOMContentLoaded', function () {
    const hubNav = document.querySelector('.hub-nav');

    if (hubNav) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 100) {
                hubNav.classList.add('scrolled');
            } else {
                hubNav.classList.remove('scrolled');
            }
        });
    }
});

// Add mouse movement effect for hub cards
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.hub-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});

// Add smooth scroll for navigation
document.querySelectorAll('.hub-nav-item').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href.startsWith('#')) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Background image rotation
const backgrounds = [
    'Mall.jpg',
    'Economic.jpg',
    'Future Technology.jpg'
];

let currentBgIndex = 0;

function rotateBackground() {
    const hero = document.querySelector('.hero');
    if (hero) {
        currentBgIndex = (currentBgIndex + 1) % backgrounds.length;
        hero.style.backgroundImage = `url('/static/images/${backgrounds[currentBgIndex]}')`;
    }
}

// Rotate background every 10 seconds
setInterval(rotateBackground, 10000);

// Add parallax effect
window.addEventListener('scroll', () => {
    const parallaxElements = document.querySelectorAll('.parallax-bg');
    parallaxElements.forEach(element => {
        const scrolled = window.pageYOffset;
        element.style.transform = `translateY(${scrolled * 0.5}px)`;
    });
}); 