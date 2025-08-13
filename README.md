# Advanced Phishing URL Detector

A modern web application that uses machine learning to detect potential phishing URLs. This project provides a user-friendly interface and robust backend for analyzing URLs for potential phishing attempts.

## Features

- Real-time URL analysis
- Machine learning-based detection
- Modern, responsive UI
- Detailed analysis results
- API endpoint for integration
- Comprehensive logging
- Health check endpoint

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Phishing-Detection-Advanced
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

5. Create the models directory and add your trained model:
```bash
mkdir models
# Add your trained model file as 'phishing_detector.joblib' in the models directory
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### Analyze URL
- **POST** `/analyze`
- Request body: `{"url": "https://example.com"}`
- Returns analysis results including prediction and confidence score

### Health Check
- **GET** `/health`
- Returns service health status and model availability

## Project Structure

```
Phishing-Detection-Advanced/
├── app.py                 # Main application file
├── feature_extractor.py   # Feature extraction module
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
├── models/               # Directory for ML models
├── static/               # Static files (CSS, JS)
│   ├── style.css
│   └── script.js
└── templates/            # HTML templates
    └── index.html
```

## Security Notes

- The application includes input validation and sanitization
- Rate limiting is recommended for production deployment
- SSL/TLS should be enabled in production
- API keys should be properly secured
- Regular updates of dependencies are recommended


## Screenshots
## User Interface
<img width="1075" height="633" alt="image" src="https://github.com/user-attachments/assets/78f89b05-96b4-449a-bc04-22028c1b855e" />

## PhishDefend – URL Scanner
-Prediction: Phishing Detected
<img width="2010" height="1514" alt="image" src="https://github.com/user-attachments/assets/8420a4fa-2832-4609-99a2-dfaf85e4a976" />

## PhishDefend – URL Scanner
-Prediction: Link is Safe
<img width="2098" height="1538" alt="image" src="https://github.com/user-attachments/assets/6d85efdb-7b4e-4b04-9f10-43383538860d" />

## Awareness Quiz
<img width="970" height="580" alt="image" src="https://github.com/user-attachments/assets/5b1d6783-1fb5-4024-8ec4-b267d98f9c8f" />

## Chatbot 
<img width="392" height="562" alt="image" src="https://github.com/user-attachments/assets/df805bb0-1cae-4f07-af36-781f3a85c185" />


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
