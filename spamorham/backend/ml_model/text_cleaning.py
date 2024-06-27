import re
import nltk
import numpy  as np
from nltk.corpus import stopwords
import pandas as pd 

def preprocess_text(x):
    x=x.to_numpy()
    tokens_list=[]
    for i in range(len(x)):
        string_x=np.array_str(x[i])
        text=string_x.lower()
        text=re.sub(r'\d+','',text)
        text=re.sub(r'[^\w\s]','',text)
        tokens=nltk.word_tokenize(text)
        tokens_list.append(tokens)
    return tokens_list

def remove_stopwords(tokens):
    filtered_tokens=[]
    for i in range(len(tokens)):
        stop_words=set(stopwords.words('english'))
        new_tokens=[word for word in tokens[i] if word not in stop_words]
        filtered_tokens.append(new_tokens)
    return filtered_tokens

def perform_lemmatization(tokens):
    lemmatized_tokens=[]
    for i in range(len(tokens)):
        lemmatizer=nltk.WordNetLemmatizer()
        lemmatized_t=[lemmatizer.lemmatize(token) for token in tokens[i] ]
        lemmatized_t=" ".join(lemmatized_t)
        lemmatized_tokens.append(lemmatized_t)
    return lemmatized_tokens

def cleaned_text(x):
    tokens=preprocess_text(x)
    filtered_tokens=remove_stopwords(tokens)
    cleaned_x=perform_lemmatization(filtered_tokens)
    return cleaned_x
