document.addEventListener('DOMContentLoaded', function() {
    var toggleButton = document.getElementById('toggleSlider');
    var toggleText = document.getElementById('toggleSliderText');
    var statusText = document.getElementById('trackingStatus');
    var isTracking = false;

    async function toggleTracking() {
        const endpoint = isTracking ? '/stop_tracking' : '/start_tracking';
        toggleText.textContent = isTracking ? 'Stop Tracking' : 'Start Tracking';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            console.log(data.status);
            isTracking = !isTracking;
            statusText.textContent = isTracking ? 'Tracking' : 'Idle';
        } catch (error) {
            console.error("Error toggling tracking:", error);
        }
    }

    toggleButton.addEventListener('click', toggleTracking);
});
