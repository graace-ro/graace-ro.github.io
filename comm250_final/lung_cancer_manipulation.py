import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
df=df.drop(columns=["Diagnosis_Date", "Patient_ID"])
df_copy = df.copy()
print(df.head())
print(df.info())
# %%
label_encoder = preprocessing.LabelEncoder()
# label_encoder.fit(df["Gender"])
# print(list(label_encoder.classes_))
# print(label_encoder.transform(df["Gender"]))
for column in df.select_dtypes(include=["str"]):
    label_encoder.fit(df_copy[column])
    print(list(label_encoder.classes_))
    print(label_encoder.transform(df_copy[column]))
    df_copy[column]=label_encoder.transform(df_copy[column])
print(df_copy.head(), df.head())
# %%
survive_colors = {0:'black', 1:'blue'}
pd.plotting.scatter_matrix(df_copy, figsize=(20, 20), grid=True, marker='o', c=df_copy['Survived'].map(survive_colors))
sns.set_theme(style="ticks")
sns.pairplot(df_copy, hue='Survived')