from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from text_cleaning import cleaned_text
from dataset_preprocessing import preprocessing
from sklearn.model_selection import train_test_split ,GridSearchCV, cross_val_score
import numpy as np
import joblib

x, y = preprocessing('ml_model\\spam_ham_dataset.csv')
y = np.ravel(y)
cleaned_x = cleaned_text(x)
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(cleaned_x).toarray()
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True, random_state=42)
clf =RandomForestClassifier()
clf.fit(x_train,y_train)
score=clf.score(x_test,y_test)
print(score)

joblib.dump(clf, "spam_or_ham.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")


