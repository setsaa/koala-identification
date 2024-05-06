// Placeholder for simulating detected animals
const animals = ["koala", "koala", "koala_teddy_bear"]; 
const animalList = document.getElementById("animalList");

animals.forEach((animal, index) => {
    const listItem = document.createElement("li");
    const img = document.createElement("img");
    img.src = `static/test${index}.jpg`;
    img.alt = `${animal} bounding box`; 
    const textNode = document.createTextNode(animal);
    
    const confidence = (Math.random() * (100 - 94) + 94).toFixed(2);
    const confidenceTextNode = document.createTextNode(` (confidence: ${confidence}%)`);

    const timeDetected = new Date().toLocaleTimeString();
    const timeDetectedTextNode = document.createTextNode(` (detected at: ${timeDetected})`);
    
    // Append the elements to the list item
    listItem.appendChild(img);
    listItem.appendChild(textNode);
    listItem.appendChild(confidenceTextNode);
    listItem.appendChild(timeDetectedTextNode);
    
    // Append the list item to the animal list
    animalList.appendChild(listItem);
});

window.onload = function() {
    // Select the video container
    const videoContainer = document.getElementById("videoContainer");

    // Create an image element
    const img = document.createElement("img");
    img.src = "static/livefeed.png";
    img.alt = "Live feed from the drone";

    // Set width and height to match the desired cropping dimensions
    img.width = 720;
    img.height = 480;

    // Centre the image
    img.style.display = "block";
    img.style.margin = "auto";
    
    // Replace the video container with the cropped image
    videoContainer.parentNode.replaceChild(img, videoContainer);

    updateDroneStats();
};

function updateDroneStats() {
    // Example: Update battery level and time
    document.getElementById("batteryLevel");
    document.getElementById("droneDate");
    document.getElementById("droneTime");
    document.getElementById("droneSpeed");
    document.getElementById("droneAltitude");
    document.getElementById("GPS");
    // Add more stat updates as needed
}