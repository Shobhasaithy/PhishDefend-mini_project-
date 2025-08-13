document.addEventListener('DOMContentLoaded', function() {
  const checkSelectedButton = document.getElementById('checkSelected');
  const checkInputButton = document.getElementById('checkInput');
  const urlInput = document.getElementById('urlInput');
  const statusDiv = document.getElementById('status');
  const featuresDiv = document.getElementById('features');

  // Function to validate URL format
  function isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  // Function to analyze URL
  async function analyzeUrl(url) {
    if (!url) {
      statusDiv.className = 'status dangerous';
      statusDiv.textContent = 'Please provide a URL to analyze';
      return;
    }

    if (!isValidUrl(url)) {
      statusDiv.className = 'status dangerous';
      statusDiv.textContent = 'Invalid URL format';
      return;
    }

    statusDiv.className = 'status loading';
    statusDiv.textContent = 'Analyzing...';
    featuresDiv.textContent = '';

    try {
      const result = await chrome.runtime.sendMessage({
        action: 'analyzeUrl',
        url: url
      });

      if (result.error) {
        statusDiv.className = 'status dangerous';
        statusDiv.textContent = `Error: ${result.error}`;
      } else {
        statusDiv.className = result.prediction === 1 ? 'status dangerous' : 'status safe';
        statusDiv.textContent = result.prediction === 1 ? 
          'Warning: This URL might be a phishing attempt!' : 
          'This URL appears to be safe.';
        
        if (result.features) {
          featuresDiv.innerHTML = '<h3>Analysis Details:</h3>' +
            Object.entries(result.features)
              .map(([key, value]) => `<div>${key}: ${value}</div>`)
              .join('');
        }
      }
    } catch (error) {
      statusDiv.className = 'status dangerous';
      statusDiv.textContent = 'Error analyzing URL';
      console.error('Error:', error);
    }
  }

  // Handle checking selected text
  checkSelectedButton.addEventListener('click', async () => {
    // Query the active tab to get selected text
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => window.getSelection().toString().trim()
    }, (results) => {
      const selectedText = results[0].result;
      if (!selectedText) {
        statusDiv.className = 'status dangerous';
        statusDiv.textContent = 'No text selected. Please select a URL on the webpage.';
        return;
      }
      analyzeUrl(selectedText);
    });
  });

  // Handle checking manually entered URL
  checkInputButton.addEventListener('click', () => {
    analyzeUrl(urlInput.value.trim());
  });

  // Handle Enter key in URL input
  urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      analyzeUrl(urlInput.value.trim());
    }
  });
});
