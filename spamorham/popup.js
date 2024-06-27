document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.sendMessage({ action: 'authenticate' }, (response) => {
        const contentDiv = document.getElementById('spinner');
        if (response.error) {
            contentDiv.textContent = 'Error: ' + response.error;
        } else {
            contentDiv.style.display = 'none';
            console.log("Predictions:", response.data['predictions']);
            const predictionsDiv = document.getElementById('content');
            response.data['predictions'].forEach(prediction => {
                const predictionDiv = document.createElement('div');
                predictionDiv.classList.add('prediction');
                
                // Conditionally add emoji based on prediction.prediction
                let emoji = '';
                if (prediction.prediction === 'Ham') {
                    emoji = '<span>🛎️</span> ';
                }

                // Construct the prediction text with emoji first if applicable
                const predictionText = `
                    <div class="email-item">
                        <h2>${emoji}<strong>Subject: </strong>${prediction.subject}</h2>
                        <p><strong>Sender: </strong>${prediction.sender}</p>
                    </div>`;

                predictionDiv.innerHTML = predictionText;
                predictionsDiv.appendChild(predictionDiv);
            });
        }
    });
});
