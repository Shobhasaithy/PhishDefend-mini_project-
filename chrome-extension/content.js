// Content script to extract additional page information if needed
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageInfo') {
    const pageInfo = {
      title: document.title,
      forms: document.forms.length,
      links: document.links.length,
      images: document.images.length,
      hasPasswordField: !!document.querySelector('input[type="password"]'),
      hasLoginForm: !!document.querySelector('form'),
    };
    sendResponse(pageInfo);
  }
  return true;
});
