document.addEventListener('DOMContentLoaded', () => {
    const urlForm = document.getElementById('urlForm');
    const urlInput = document.getElementById('urlInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');
    const errorAlert = document.getElementById('errorAlert');

    urlForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI state
        hideError();
        hideResult();
        showLoading();

        const url = urlInput.value.trim();

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to analyze URL');
            }

            const result = await response.json();
            displayResult(result);
        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    function displayResult(result) {
        const isPhishing = result.is_phishing;
        const confidence = (result.confidence * 100).toFixed(2);
        
        const resultHtml = `
            <div class="text-center mb-4">
                <i class="fas fa-${isPhishing ? 'exclamation-triangle fa-3x result-danger' : 'check-circle fa-3x result-safe'}"></i>
            </div>
            <div class="alert ${isPhishing ? 'alert-danger' : 'alert-success'} text-center">
                <h4 class="alert-heading">
                    ${isPhishing ? 'Potential Phishing Detected!' : 'URL Appears Safe'}
                </h4>
                <p class="mb-0">
                    Confidence: ${confidence}%
                </p>
            </div>
            <div class="mt-3">
                <h5>Analyzed URL:</h5>
                <p class="text-break">${escapeHtml(urlInput.value)}</p>
                <p class="text-muted small">
                    Analysis timestamp: ${new Date(result.timestamp).toLocaleString()}
                </p>
            </div>
            ${isPhishing ? `
                <div class="alert alert-warning mt-3">
                    <i class="fas fa-info-circle"></i>
                    <strong>Warning:</strong> This URL shows characteristics commonly associated with phishing attempts.
                    Exercise extreme caution and verify the source before proceeding.
                </div>
            ` : ''}
        `;

        resultContent.innerHTML = resultHtml;
        showResult();
    }

    function showLoading() {
        loadingSpinner.classList.remove('d-none');
    }

    function hideLoading() {
        loadingSpinner.classList.add('d-none');
    }

    function showResult() {
        resultCard.classList.remove('d-none');
    }

    function hideResult() {
        resultCard.classList.add('d-none');
    }

    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.classList.remove('d-none');
    }

    function hideError() {
        errorAlert.classList.add('d-none');
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
