# Emotion Detector App 🎭

A modern web application that detects emotions from text input using machine learning. The app features a beautiful UI with animations and provides real-time emotion analysis.

## Features

- Text-based emotion detection
- Support for 6 different emotions (Joy, Sadness, Anger, Fear, Love, Surprise)
- Interactive visualization of emotion probabilities
- Modern UI with animations
- Real-time analysis
- No external API dependencies

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/emotion-detector.git
cd emotion-detector
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your text in the input field and click "Analyze Emotions" to see the results!

## How it Works

The emotion detection model uses:
- TF-IDF vectorization for text feature extraction
- Logistic Regression for classification
- Custom text preprocessing using neattext
- Streamlit for the web interface
- Plotly for interactive visualizations

## Model Details

The current implementation includes a basic model trained on a sample dataset. The model can detect the following emotions:
- Joy 😊
- Sadness 😢
- Anger 😠
- Fear 😨
- Love ❤️
- Surprise 😲

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 