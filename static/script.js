// script.js

function startAssistant() {
    fetch('/process_audio', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.type === 'gif') {
            displayGif(data.value);
        } else if (data.type === 'image') {
            displayImage(data.value);
        }
    });
}

function displayGif(value) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<p>${value}</p><img src="/static/ISL_Gifs/${value.toLowerCase()}.gif" alt="${value} gif">`;
}

function displayImage(value) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<p>${value}</p><img src="/static/letters/${value.toLowerCase()}.jpg" alt="${value} image">`;
}

