# Phishing Detection Chrome Extension

This Chrome extension uses machine learning to detect potential phishing websites in real-time. It works in conjunction with the Python-based ML backend to provide accurate phishing detection.

## Features

- Real-time website analysis
- Visual indicators for potentially dangerous sites
- Detailed feature analysis view
- Automatic checking of newly loaded pages
- Manual check option via popup

## Installation

1. Make sure the Python backend server is running:
   ```bash
   cd ..
   python app.py
   ```

2. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" in the top right
   - Click "Load unpacked"
   - Select this directory (chrome-extension)

## Usage

1. The extension will automatically check each website you visit
2. A red warning badge will appear on the extension icon for suspicious sites
3. Click the extension icon to see detailed analysis
4. Use the "Check This Page" button to manually recheck any page

## Requirements

- Chrome browser
- Python backend server running on localhost:5000
- Active internet connection

## Note

Make sure the Python backend server (app.py) is running before using the extension, as it relies on the ML model for predictions.
