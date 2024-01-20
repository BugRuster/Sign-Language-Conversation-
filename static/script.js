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
                // displayImage(data.value);
                for (let i = 0; i < data.value.length; i++) {
                    // displayImage(data.value[i]);
                    setTimeout(() => {
                        displayImage(data.value[i]);
                    }, i * 800);

                }

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

