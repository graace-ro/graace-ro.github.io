import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
df=df.drop(columns=["Diagnosis_Date", "Patient_ID"])
print(df.head())
print(df.info())
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(df["Gender"])
print(list(label_encoder.classes_))
print(label_encoder.transform(df["Gender"]))