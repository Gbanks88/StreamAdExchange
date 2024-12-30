document.addEventListener('DOMContentLoaded', function () {
    // Check if we're on the Digital Market Hub page
    if (window.location.pathname.includes('Digital Market Hub')) {
        // Initialize market data updates
        updateMarketData();
        // Update every 5 seconds
        setInterval(updateMarketData, 5000);
    }
});

function updateMarketData() {
    fetch('/service/Digital Market Hub/data')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateUI(data);
            } else {
                console.warn('Market data status:', data.status, data.error);
                // Update UI to show fallback/error state
                showFallbackState(data);
            }
        })
        .catch(error => {
            console.error('Error fetching market data:', error);
            showErrorState();
        });
}

function updateUI(data) {
    // Update price and trend
    const priceElement = document.getElementById('market-price');
    if (priceElement) {
        priceElement.textContent = `$${data.price}`;
        priceElement.className = `price-value ${data.prediction === 'uptrend' ? 'trend-up' : 'trend-down'}`;
    }

    // Update prediction confidence
    const confidenceElement = document.getElementById('ai-confidence');
    if (confidenceElement) {
        confidenceElement.textContent = `${data.confidence}% confidence (${data.mode})`;
    }

    // Update volume
    const volumeElement = document.getElementById('market-volume');
    if (volumeElement) {
        volumeElement.textContent = data.volume.toLocaleString();
    }
}

function showFallbackState(data) {
    const elements = ['market-price', 'ai-confidence', 'market-volume'];
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('fallback-mode');
        }
    });
}

function showErrorState() {
    const elements = ['market-price', 'ai-confidence', 'market-volume'];
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = 'Data unavailable';
            element.classList.add('error-state');
        }
    });
} 