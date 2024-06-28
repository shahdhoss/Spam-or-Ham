chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed or updated.');
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'authenticate') {
      authenticateUser(sendResponse);
      return true;
  }
});

function authenticateUser(callback) {
  chrome.identity.getAuthToken({ interactive: true }, (token) => {
    let redirectUri = chrome.identity.getRedirectURL();
    console.log('Redirect URI:', redirectUri); // For debugging

      if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError.message);
          callback({ error: chrome.runtime.lastError.message });
          return;
      }
      console.log('Authentication token:', token);
      fetch('http://127.0.0.1:5000/', {
          method: 'GET',
          headers: {
              'Authorization': 'Bearer ' + token
          }
      })
      .then(response => response.json())
      .then(data => {
          callback({ data: data });
      })
      .catch(error => {
          console.error('Error fetching data:', error);
          callback({ error: error.toString() });
      });
  });
}

async function checkForNotifications() {
  try {
    const response = await fetch('https://<your-service-url>/get-notifications');
    const data = await response.json();
    if (data.newEmails) {
      chrome.notifications.create('gmail-notification', {
        type: 'basic',
        iconUrl: 'icon.png',
        title: 'New Email',
        message: 'You have a new email!'
      });
    }
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
}

chrome.runtime.onStartup.addListener(checkForNotifications);
chrome.runtime.onInstalled.addListener(checkForNotifications);
setInterval(checkForNotifications, 60000);  // Check every minute









  