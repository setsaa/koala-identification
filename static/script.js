document.addEventListener('DOMContentLoaded', function() {
    var liveVideo = document.getElementById('liveVideo');
    var toggleButton = document.getElementById('toggleSlider');
    var statusText = document.getElementById('trackingStatus');
    var isTracking = false;

    async function toggleTracking() {
        const endpoint = isTracking ? '/stop_tracking' : '/start_tracking';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (data.status !== "No koalas found") {  // Check if the response is not the no koalas message
                isTracking = !isTracking;
                toggleButton.textContent = isTracking ? 'Stop Tracking' : 'Start Tracking';
                statusText.textContent = 'Status: ' + (isTracking ? 'Tracking' : 'Idle');
                updateDetectedAnimals();  // Call to update the animal list immediately after toggling
            } else {
                statusText.textContent = 'Status: No koalas found';
            }
            checkVideoFeed();
        } catch (error) {
            console.error("Error toggling tracking:", error);
        }
    }

    function checkVideoFeed() {
        fetch('/video_feed').then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            liveVideo.src = '/video_feed';
        }).catch(error => {
            console.error('Problem with the video feed:', error);
            liveVideo.src = '/static/default.png';
        });
    }

    toggleButton.addEventListener('click', toggleTracking);

    function updateDetectedAnimals() {
        fetch('/detected_koalas')
            .then(response => response.json())
            .then(data => {
                if (data.status === "No koalas found") {
                    statusText.textContent = 'Status: No koalas found';
                    return;  // Do not update the list if no koalas are found
                }
                const animalList = document.getElementById('animalList');
                animalList.innerHTML = '';  // Clear the current list
                data.forEach(animal => {
                    const li = document.createElement('li');
                    li.textContent = `${animal.label} (${(animal.confidence * 100).toFixed(2)}%)`;
                    animalList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching animals:', error));
    }

    setInterval(updateDetectedAnimals, 5000);  // Update the list every 5 seconds
    checkVideoFeed();  // Initial check on load
});
