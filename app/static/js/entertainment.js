// Function to update stock prices
function updateStockPrices() {
    // In a real application, this would fetch from an API
    const stocks = document.querySelectorAll('.stock-price');
    stocks.forEach(stock => {
        const random = Math.random();
        if (random > 0.5) {
            stock.classList.remove('text-danger');
            stock.classList.add('text-success');
            stock.innerHTML = `$${(Math.random() * 1000).toFixed(2)} <i class="bi bi-arrow-up"></i>`;
        } else {
            stock.classList.remove('text-success');
            stock.classList.add('text-danger');
            stock.innerHTML = `$${(Math.random() * 1000).toFixed(2)} <i class="bi bi-arrow-down"></i>`;
        }
    });
}

// Function to update viewer counts
function updateViewerCounts() {
    const viewers = document.querySelectorAll('.viewer-count');
    viewers.forEach(viewer => {
        const count = Math.floor(Math.random() * 20000);
        viewer.textContent = `${(count/1000).toFixed(1)}K viewers`;
    });
}

// Update every 5 seconds
setInterval(updateStockPrices, 5000);
setInterval(updateViewerCounts, 5000);

// Entertainment page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Your entertainment page JavaScript code here
    console.log('Entertainment page loaded');
}); 