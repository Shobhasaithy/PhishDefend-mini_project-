// Configuration for the API endpoint
const API_ENDPOINT = 'http://localhost:5000/analyze';

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzeUrl') {
    analyzeUrl(request.url)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Will respond asynchronously
  }
});

// Function to analyze a URL using our API
async function analyzeUrl(url) {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const data = await response.json();
    return {
      prediction: data.prediction,
      features: data.features,
      probability: data.probability
    };
  } catch (error) {
    console.error('Error analyzing URL:', error);
    throw new Error('Failed to analyze URL');
  }
}
