// Placeholder for simulating detected animals
const animals = ["Koala", "Koala", "Koala teddy bear"]; 
const animalList = document.getElementById("animalList");

animals.forEach((animal, index) => {
    const listItem = document.createElement("li");
    const img = document.createElement("img");
    img.src = index === 2 ? "static/test2.jpg" : "static/test1.jpg";
    img.alt = `${animal} bounding box`; 
    const textNode = document.createTextNode(animal);
    listItem.appendChild(img);
    listItem.appendChild(textNode);
    animalList.appendChild(listItem);
});