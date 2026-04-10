import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
#print(df.columns)
numeric_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(include="str").columns
#print(numeric_cols)
#print(categorical_cols)
df['Numeric_Outlier'] = 'False'
for group_value in ['No','Yes']:
    group = df[df['Survived']==group_value]
    for col in numeric_cols:
        z = np.abs(stats.zscore(group[col]))
        outlier_mask = (z>3)
        df.loc[group.index[outlier_mask], 'Numeric_Outlier'] = True
print(df.columns)

df['Categorical_Outlier'] = 'False'
for group_value in ['No','Yes']:
    group = df[df['Survived']==group_value]
    for col in categorical_cols:
        freq = group[col].value_counts(normalize=True)
        rare_categories = freq[freq<0.05].index
        group_mask = group[col].isin(rare_categories)
        df.loc[group.index[group_mask], 'Categorical_Outlier']=True
df['Is_Outlier'] = df['Categorical_Outlier'] | df['Numeric_Outlier']
print(df.head())
