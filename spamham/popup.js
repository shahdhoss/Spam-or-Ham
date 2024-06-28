document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.sendMessage({ action: 'authenticate' }, (response) => {
        const contentDiv = document.getElementById('spinner');
        const errorContainer= document.getElementById('errorContainer')
        if (response.error) {
            contentDiv.style.display='none'
            const errorMessage = document.createElement('h2')
            errorMessage.textContent = 'Server not responsive :('
            errorContainer.style.display ='flex'
            errorContainer.appendChild(errorMessage)
        } else {
            contentDiv.style.display = 'none';
            if (response.data['predictions']==undefined){
                const no_emails=document.createElement('h1')
                errorContainer.textContent='No new emails!😼'
                errorContainer.style.display='flex'
                errorContainer.appendChild(no_emails)
            }
            console.log("Predictions:", response.data['predictions']);
            const predictionsDiv = document.getElementById('content');
            response.data['predictions'].forEach(prediction => {
                const predictionDiv = document.createElement('div');
                predictionDiv.classList.add('prediction');
                let emoji = '';
                if (prediction.prediction === 'Ham') {
                    emoji = '<span>🛎️</span> ';
                }
                const predictionText = `
                    <div class="email-item">
                        <a href="https://mail.google.com/mail/u/0/#inbox/${prediction.message_id}" target="_blank" class="email-link">
                            <h2>${emoji}<strong>Subject: </strong>${prediction.subject}</h2>
                    </a>    
                        <p><strong>Sender: </strong>${prediction.sender}</p>
                    </div>`;

                predictionDiv.innerHTML = predictionText;
                predictionsDiv.appendChild(predictionDiv);
            });
        }
    });
});
