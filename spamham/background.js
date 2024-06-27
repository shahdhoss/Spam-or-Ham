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
      fetch('http://localhost:5000/', {
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









  