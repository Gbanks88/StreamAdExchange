document.addEventListener('DOMContentLoaded', function() {
    // Random glow colors for certain elements
    const glowElements = document.querySelectorAll('.feature-icon');
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];
    
    setInterval(() => {
        glowElements.forEach(element => {
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            element.style.textShadow = `0 0 10px ${randomColor}`;
        });
    }, 1000);
}); 