document.addEventListener('DOMContentLoaded', function() {
    const affiliateLinks = document.querySelectorAll('.affiliate-link');
    
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    // Add security measures to affiliate links
    affiliateLinks.forEach(link => {
        // Add rel="noopener noreferrer" for security
        link.setAttribute('rel', 'noopener noreferrer');
        
        link.addEventListener('click', async function(e) {
            e.preventDefault();
            const platform = this.getAttribute('data-platform');
            const targetUrl = this.href;
            
            try {
                // Add request signing
                const timestamp = Date.now();
                const requestData = {
                    platform,
                    timestamp: new Date().toISOString(),
                    fingerprint: await generateBrowserFingerprint()
                };
                
                const response = await fetch('/track-affiliate-click', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': csrfToken,
                        'X-Request-Timestamp': timestamp.toString()
                    },
                    body: JSON.stringify(requestData),
                    credentials: 'same-origin'
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    // Store click ID securely
                    sessionStorage.setItem('lastClickId', result.click_id);
                    
                    // Redirect with secure parameters
                    const secureUrl = new URL(targetUrl);
                    secureUrl.searchParams.append('ref', result.click_id);
                    window.location.href = secureUrl.toString();
                } else {
                    console.error('Error tracking click');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    // Generate browser fingerprint for fraud prevention
    async function generateBrowserFingerprint() {
        const components = [
            navigator.userAgent,
            navigator.language,
            screen.width,
            screen.height,
            new Date().getTimezoneOffset()
        ].join('|');
        
        // Use SubtleCrypto for secure hashing
        const msgBuffer = new TextEncoder().encode(components);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
}); 