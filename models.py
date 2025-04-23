from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import pandas as pd

# Train and save model pipeline
def train_email_classifier(csv_path: str):
    df = pd.read_csv(csv_path)
    X = df['email']
    y = df['type']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=10000)),
        ('clf', LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, 'email_classifier.pkl')
    print("\nModel saved as 'email_classifier.pkl'")

# Load and predict

def load_model():
    return joblib.load('email_classifier.pkl')

def predict_category(model, text):
    return model.predict([text])[0]
