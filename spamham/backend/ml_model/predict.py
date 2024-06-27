import pandas as pd
import joblib
from text_cleaning import cleaned_text

def load(message,file):
    cleaned_x=cleaned_text(message)
    vectorizer=joblib.load("vectorizer.joblib")
    x = vectorizer.transform(cleaned_x).toarray()
    loaded_clf = joblib.load(file)
    prediction = loaded_clf.predict(x)
    return prediction

def predicts(message):
    spam_ham =pd.DataFrame([message])
    prediction = load(spam_ham,'spam_or_ham.joblib')
    # print(f"Message: {spam_ham}", f"Prediction:{prediction}")
    return prediction