import requests
import json
from urllib.parse import urlparse
from tabulate import tabulate
import time

def analyze_url_features(url):
    """Analyze basic URL features for display."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "has_ip": any(c.isdigit() for c in parsed.netloc),
        "length": len(url),
        "num_dots": url.count('.'),
        "has_suspicious_words": any(word in url.lower() for word in ['secure', 'login', 'signin', 'bank', 'account']),
    }

def test_url(url):
    """Test a URL with our phishing detection API and show detailed analysis."""
    try:
        # Analyze URL features
        features = analyze_url_features(url)
        
        # Make API request
        response = requests.post(
            'http://localhost:5000/analyze',
            json={'url': url}
        )
        
        print(f"\n{'='*70}")
        print(f"Testing URL: {url}")
        print(f"{'='*70}")
        
        # Print URL analysis
        feature_table = [[k, v] for k, v in features.items()]
        print("\nURL Analysis:")
        print(tabulate(feature_table, headers=['Feature', 'Value'], tablefmt='grid'))
        
        if response.status_code == 200:
            result = response.json()
            
            # Print prediction results
            print("\nPrediction Results:")
            prediction_table = [
                ['Classification', 'Potential Phishing' if result['is_phishing'] else 'Legitimate'],
                ['Confidence', f"{result['confidence']*100:.2f}%"],
                ['Timestamp', result['timestamp']]
            ]
            print(tabulate(prediction_table, headers=['Metric', 'Value'], tablefmt='grid'))
            
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
    
    print(f"\n{'-'*70}")
    time.sleep(1)  # Add delay between requests

# Test URLs
test_urls = [
    # Known legitimate URLs
    "https://www.google.com",
    "https://www.microsoft.com",
    
    # Suspicious URLs
    "http://googgle.com",  # Typosquatting
    "http://secure.login.account-verify.com",  # Suspicious words
    "http://192.168.1.1/login.php",  # IP address
    
    # Complex URLs
    "https://subdomain.example.com/path/to/page?param=value",
    "https://login.secure.banking.example.com/account",
    
    # Invalid URLs
    "not_a_valid_url",
]

print("\nStarting Comprehensive URL Testing...")
print("This test will analyze various URLs and show detailed feature analysis")
print("=" * 70)

for url in test_urls:
    test_url(url)

print("\nTesting completed!")
print("Note: High confidence in phishing detection for legitimate sites may indicate")
print("that the model needs retraining with more balanced data.")
