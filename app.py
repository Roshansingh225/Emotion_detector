import streamlit as st
import plotly.express as px
import pandas as pd
from emotion_model import EmotionDetector
import time

# Set page config
st.set_page_config(
    page_title="Emotion Detector",
    page_icon="🎭",
    layout="wide",
    menu_items={},  # This removes the three-dot menu
    initial_sidebar_state="collapsed"  # This hides the sidebar
)

# Hide deploy button and other Streamlit components
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        [data-testid="stDecoration"] {visibility: hidden !important;}
        [data-testid="stHeader"] {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# Background image in base64
background_image = """
data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPgogIDxkZWZzPgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJncmFkIiBncmFkaWVudFRyYW5zZm9ybT0icm90YXRlKDQ1KSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmM2U3ZTk7IHN0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjUwJSIgc3R5bGU9InN0b3AtY29sb3I6I2U3ZWRmNjsgc3RvcC1vcGFjaXR5OjEiIC8+CiAgICAgIDxzdG9wIG9mZnNldD0iMTAwJSIgc3R5bGU9InN0b3AtY29sb3I6I2U3ZjBmZDsgc3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPHBhdHRlcm4gaWQ9InBhdHRlcm4iIHg9IjAiIHk9IjAiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgICAgIDxjaXJjbGUgY3g9IjMwIiBjeT0iMzAiIHI9IjIwIiBmaWxsPSJyZ2JhKDI1NSwgMjU1LCAyNTUsIDAuMSkiLz4KICAgIDwvcGF0dGVybj4KICA8L2RlZnM+CiAgPHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmFkKSIvPgogIDxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjcGF0dGVybikiLz4KPC9zdmc+"""

# Custom CSS for modern design
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    .main-container {{
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.2) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        margin: -1rem;
    }}
    
    .css-1d391kg {{
        padding: 2rem 1rem;
    }}
    
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid rgba(224, 224, 224, 0.8);
        padding: 15px;
        font-size: 16px;
    }}
    
    .stButton > button {{
        background: linear-gradient(45deg, #ff4b4b 0%, #ff6b6b 100%);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-size: 16px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(45deg, #ff3333 0%, #ff5555 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.3);
    }}
    
    .emotion-card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        margin: 15px 0;
        color: #000000;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease;
    }}
    
    .emotion-card:hover {{
        transform: translateY(-5px);
    }}
    
    .emotion-list {{
        list-style-type: none;
        padding-left: 0;
        color: #000000;
    }}
    
    .emotion-list li {{
        margin: 15px 0;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        border-radius: 12px;
        transition: all 0.3s ease;
        background-color: rgba(248, 249, 250, 0.9);
        color: #000000;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }}
    
    .emotion-list li:hover {{
        transform: translateX(5px);
        background-color: rgba(240, 241, 242, 0.95);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }}
    
    .emotion-emoji {{
        font-size: 28px;
        display: inline-block;
        animation: pulse 2s infinite;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}
    
    .about-description {{
        color: #000000;
        line-height: 1.8;
        margin: 20px 0;
        font-weight: 400;
        font-size: 16px;
    }}
    
    .about-title {{
        color: #000000;
        font-size: 1.8em;
        margin-bottom: 20px;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 10px;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .main-title {{
        animation: fadeIn 1s ease-out;
    }}
    
    div[data-testid="stVerticalBlock"] {{
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }}
</style>
""", unsafe_allow_html=True)

# Initialize emotion detector
@st.cache_resource
def load_emotion_detector():
    detector = EmotionDetector()
    if not detector.load_model():
        detector.train_model()
    return detector

# Title with animation
def animated_title():
    st.markdown("""
        <h1 class='main-title' style='text-align: center; color: #333; font-size: 3em; margin-bottom: 1.5em;'>
            <span style='display: inline-block; animation: bounce 1s infinite;'>🎭</span> 
            Emotion Detector
        </h1>
        <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    animated_title()
    
    detector = load_emotion_detector()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class='emotion-card'>
                <h3 style='color: #333;'>Enter your text:</h3>
            </div>
        """, unsafe_allow_html=True)
        
        text_input = st.text_area(
            "Text Input",
            height=150,
            placeholder="Type something here...",
            label_visibility="collapsed"
        )
        
        if st.button("Analyze Emotions"):
            if text_input.strip():
                with st.spinner("Analyzing emotions..."):
                    # Add a small delay for animation effect
                    time.sleep(0.5)
                    prediction, emotion_probs = detector.predict_emotion(text_input)
                    
                    # Create emotion probability chart
                    emotions_df = pd.DataFrame({
                        'Emotion': list(emotion_probs.keys()),
                        'Probability': list(emotion_probs.values())
                    })
                    
                    fig = px.bar(
                        emotions_df,
                        x='Emotion',
                        y='Probability',
                        color='Emotion',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    fig.update_layout(
                        title={
                            'text': "Emotion Analysis Results",
                            'y':0.95,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                        },
                        xaxis_title="",
                        yaxis_title="Confidence",
                        showlegend=False
                    )
                    
                    # Display results
                    st.markdown(f"""
                        <div class='emotion-card'>
                            <h3 style='color: #333;'>Detected Emotion: 
                                <span style='color: #ff4b4b; font-size: 1.2em;'>{prediction.title()}</span>
                            </h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please enter some text to analyze.")
    
    with col2:
        st.markdown("""
            <div class='emotion-card'>
                <h3 class='about-title'>About This App</h3>
                <p class='about-description'>
                    Welcome to the Emotion Detector! This AI-powered tool analyzes text to identify emotions using advanced natural language processing techniques.
                </p>
                <p class='about-description'>
                    Our model can detect six primary emotions with high accuracy:
                </p>
                <ul class='emotion-list'>
                    <li><span class='emotion-emoji'>😊</span> Joy - Happiness, excitement, and positive feelings</li>
                    <li><span class='emotion-emoji'>😢</span> Sadness - Sorrow, disappointment, and melancholy</li>
                    <li><span class='emotion-emoji'>😠</span> Anger - Frustration, annoyance, and rage</li>
                    <li><span class='emotion-emoji'>😨</span> Fear - Anxiety, worry, and apprehension</li>
                    <li><span class='emotion-emoji'>❤️</span> Love - Affection, care, and attachment</li>
                    <li><span class='emotion-emoji'>😲</span> Surprise - Astonishment, amazement, and shock</li>
                </ul>
                <p class='about-description'>
                    Simply type or paste your text in the input field and click "Analyze Emotions" to see the emotional analysis results with confidence scores!
                </p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 