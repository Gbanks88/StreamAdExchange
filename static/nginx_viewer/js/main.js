// Global variables
let currentSection = 'live';
let liveLogsEventSource = null;
let charts = {};

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function () {
    showSection('live');
    initializeLiveLogs();
    updateStats();
    loadErrors();
});

// Section visibility control
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });

    // Show selected section
    document.getElementById(`${sectionName}-section`).classList.remove('hidden');
    currentSection = sectionName;

    // Handle section-specific initialization
    if (sectionName === 'live') {
        initializeLiveLogs();
    } else if (sectionName === 'stats') {
        updateStats();
    } else if (sectionName === 'errors') {
        loadErrors();
    }
}

// Live logs handling
function initializeLiveLogs() {
    const logsContainer = document.getElementById('live-logs');

    // Close existing connection if any
    if (liveLogsEventSource) {
        liveLogsEventSource.close();
    }

    // Connect to SSE endpoint
    liveLogsEventSource = new EventSource('/api/logs/live');

    liveLogsEventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);

        // Skip keepalive messages
        if (data.keepalive) return;

        // Create log entry
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.innerHTML = `
            <span class="timestamp">${data.timestamp}</span>
            <span class="method ${data.method.toLowerCase()}">${data.method}</span>
            <span class="path">${data.path}</span>
            <span class="status status-${data.status.charAt(0)}xx">${data.status}</span>
        `;

        // Add to container and scroll
        logsContainer.appendChild(logEntry);
        logsContainer.scrollTop = logsContainer.scrollHeight;

        // Keep only last 1000 entries
        while (logsContainer.children.length > 1000) {
            logsContainer.removeChild(logsContainer.firstChild);
        }
    };
}

// Statistics handling
function updateStats() {
    const hours = document.getElementById('time-range').value;

    fetch(`/api/stats?hours=${hours}`)
        .then(response => response.json())
        .then(data => {
            updateRequestsChart(data);
            updateStatusChart(data);
            updateMethodsChart(data);
        });
}

function updateRequestsChart(data) {
    const requestsData = {
        x: Object.keys(data.requests_by_path),
        y: Object.values(data.requests_by_path),
        type: 'bar',
        name: 'Requests by Path'
    };

    const layout = {
        title: 'Requests by Path',
        xaxis: { tickangle: -45 },
        yaxis: { title: 'Number of Requests' }
    };

    Plotly.newPlot('requests-chart', [requestsData], layout);
}

function updateStatusChart(data) {
    const statusData = {
        labels: Object.keys(data.status_codes),
        values: Object.values(data.status_codes),
        type: 'pie',
        name: 'Status Codes'
    };

    const layout = {
        title: 'Status Code Distribution'
    };

    Plotly.newPlot('status-chart', [statusData], layout);
}

function updateMethodsChart(data) {
    const methodsData = {
        x: Object.keys(data.methods),
        y: Object.values(data.methods),
        type: 'bar',
        name: 'HTTP Methods'
    };

    const layout = {
        title: 'HTTP Methods Distribution',
        yaxis: { title: 'Number of Requests' }
    };

    Plotly.newPlot('methods-chart', [methodsData], layout);
}

// Error log handling
function loadErrors() {
    fetch('/api/errors')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('error-summary');
            container.innerHTML = '';

            Object.entries(data).forEach(([level, errors]) => {
                const levelDiv = document.createElement('div');
                levelDiv.className = `error-level ${level.toLowerCase()}`;
                levelDiv.innerHTML = `<h3>${level} (${errors.length})</h3>`;

                errors.forEach(error => {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-entry';
                    errorDiv.innerHTML = `
                        <span class="timestamp">${error.timestamp}</span>
                        <span class="message">${error.message}</span>
                    `;
                    levelDiv.appendChild(errorDiv);
                });

                container.appendChild(levelDiv);
            });
        });
}

// Search functionality
function searchLogs() {
    const pattern = document.getElementById('search-input').value;
    const logType = document.getElementById('log-type').value;

    if (!pattern) return;

    fetch(`/api/search?pattern=${encodeURIComponent(pattern)}&type=${logType}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('search-results');
            container.innerHTML = '';

            data.forEach(line => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'search-result';
                resultDiv.textContent = line;
                container.appendChild(resultDiv);
            });

            if (data.length === 0) {
                container.innerHTML = '<div class="no-results">No matches found</div>';
            }
        });
}

// Add some keyboard shortcuts
document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case 'l':
                e.preventDefault();
                showSection('live');
                break;
            case 's':
                e.preventDefault();
                showSection('stats');
                break;
            case 'e':
                e.preventDefault();
                showSection('errors');
                break;
            case 'f':
                e.preventDefault();
                showSection('search');
                document.getElementById('search-input').focus();
                break;
        }
    }
}); 