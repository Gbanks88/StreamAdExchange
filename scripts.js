document.addEventListener('DOMContentLoaded', () => {
    const ticker = document.querySelector('.ticker');

    // Dummy data, replace with actual API call
    const stockData = [
        { name: 'Dow Jones', value: '34,000' },
        { name: 'S&P 500', value: '4,200' },
        { name: 'Nasdaq', value: '13,500' }
    ];

    ticker.innerHTML = stockData.map(stock => `<div class="ticker-item">${stock.name}: ${stock.value}</div>`).join('');

    // To use actual API, uncomment and modify the following:
    // fetch('API_URL')
    //     .then(response => response.json())
    //     .then(data => {
    //         const stockData = processStockData(data); // Implement this function to process API data
    //         ticker.innerHTML = stockData.map(stock => `<div class="ticker-item">${stock.name}: ${stock.value}</div>`).join('');
    //     });
});
