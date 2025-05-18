import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import neattext.functions as nfx
import joblib
import os

class EmotionDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression(random_state=42)
        self.emotions = ['joy', 'sadness', 'anger', 'fear', 'love', 'surprise']
        
    def clean_text(self, text):
        text = str(text).lower()
        text = nfx.remove_punctuations(text)
        text = nfx.remove_special_characters(text)
        text = nfx.remove_stopwords(text)
        return text
    
    def train_model(self):
        # Sample training data (you can replace this with your own dataset)
        data = {
            'text': [
                "I am so happy today!", "This is the best day ever!", "I love spending time with you",
                "I feel so sad and lonely", "This is devastating news", "I miss you terribly",
                "I am furious right now!", "This makes me so angry!", "I hate this situation",
                "I am terrified", "This is so scary", "I'm afraid of what might happen",
                "You mean the world to me", "I love you so much", "You're amazing",
                "Wow! I didn't expect that!", "This is incredible!", "I'm shocked!"
            ],
            'emotion': [
                'joy', 'joy', 'joy',
                'sadness', 'sadness', 'sadness',
                'anger', 'anger', 'anger',
                'fear', 'fear', 'fear',
                'love', 'love', 'love',
                'surprise', 'surprise', 'surprise'
            ]
        }
        
        df = pd.DataFrame(data)
        df['clean_text'] = df['text'].apply(self.clean_text)
        
        X = self.vectorizer.fit_transform(df['clean_text'])
        y = df['emotion']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Save the model and vectorizer
        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(self.model, 'models/emotion_model.joblib')
        joblib.dump(self.vectorizer, 'models/vectorizer.joblib')
        
        return self.model, self.vectorizer
    
    def load_model(self):
        if os.path.exists('models/emotion_model.joblib') and os.path.exists('models/vectorizer.joblib'):
            self.model = joblib.load('models/emotion_model.joblib')
            self.vectorizer = joblib.load('models/vectorizer.joblib')
            return True
        return False
    
    def predict_emotion(self, text):
        clean_text = self.clean_text(text)
        text_vectorized = self.vectorizer.transform([clean_text])
        prediction = self.model.predict(text_vectorized)[0]
        probabilities = self.model.predict_proba(text_vectorized)[0]
        emotion_probs = dict(zip(self.model.classes_, probabilities))
        return prediction, emotion_probs

if __name__ == "__main__":
    detector = EmotionDetector()
    detector.train_model() 