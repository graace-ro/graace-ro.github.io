# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
df_copy = df.copy()
df_copy=df_copy.drop(columns=["Diagnosis_Date", "Patient_ID", "Diagnosis_Year"])
print(df_copy.head())
print(df_copy.info())
print(df_copy.columns)
df.describe()

# %%
label_encoder = preprocessing.LabelEncoder()
# label_encoder.fit(df["Gender"])
# print(list(label_encoder.classes_))
# print(label_encoder.transform(df["Gender"]))
for column in df_copy.select_dtypes(include=["str"]):
    label_encoder.fit(df_copy[column])
    #print(list(label_encoder.classes_))
    #print(label_encoder.transform(df_copy[column]))
    df_copy[column]=label_encoder.transform(df_copy[column])
#print(df_copy.head(), df.head())
# %%
pd.plotting.scatter_matrix(df_copy[['Age', 'Gender', 'Smoking_Status', 'Years_Smoking', 'Family_History', 'Air_Pollution_Exposure', 'Survived']], figsize=(20,20))
#plt.show()
# %%
survivors = df_copy[df_copy['Survived']==0]
deceased = df_copy[df_copy['Survived']==1]
print(survivors.head())
print(deceased.head())
# %%
