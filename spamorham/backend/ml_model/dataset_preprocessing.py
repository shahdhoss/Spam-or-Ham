import numpy as np
import pandas as pd

def preprocessing(file):
    df = pd.read_csv(file)
    df=df.drop(["label","Unnamed: 0"],axis=1)
    text = 'text'
    subject = 'Subject: '
    df[text] = df[text].str.replace(subject, '', regex=False)

    x=df.iloc[:,:1]
    y=df.iloc[:,1:2]
    return x,y
