import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
df = df.drop(columns=['Patient_ID', 'Diagnosis_Date'])
#print(df.columns)
numeric_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(include="str").columns
#print(numeric_cols)
#print(categorical_cols)
df['Outlier_Reason'] = ''
df['Numeric_Outlier'] = False #sets every entry in this new column to false
for group_value in ['No','Yes']: #for the answers of no and yes
    group = df[df['Survived']==group_value] #the group of this iteration is the group that is either yes or no
    for col in numeric_cols: #for the numeric columns
        z = np.abs(stats.zscore(group[col])) #get the z score of all the nos for that column and all the yes's for that column
        outlier_mask = (z>3) #a boolean series of which values have a z score (deviation) that is greater than 3, which makes it an outlier
        outlier_index = group.index[outlier_mask]
        df.loc[outlier_index, 'Numeric_Outlier'] = True #the indeces of these values, for that group, is set to true
        df.loc[outlier_index, 'Outlier_Reason'] += (col + '=' + df.loc[outlier_index,col].astype(str) + '; ')
#print(df.columns)

df['Categorical_Outlier'] = False
for group_value in ['No','Yes']:
    group = df[df['Survived']==group_value]
    for col in categorical_cols:
        freq = group[col].value_counts(normalize=True) #finding the frequency of the categorical variable
        rare_categories = freq[freq<0.05].index #a rare category is one whose frequency is <0.05. we get the indeces of these rare categories
        group_mask = group[col].isin(rare_categories) #making a mask like above for the rows that are rare categories
        outlier_index = group.index[group_mask]
        df.loc[outlier_index, 'Categorical_Outlier']=True #set those rows to true
        df.loc[outlier_index, 'Outlier_Reason'] += (col + '=' + df.loc[outlier_index, col].astype(str) + '; ')
df['Is_Outlier'] = df['Categorical_Outlier'] | df['Numeric_Outlier'] #combine the categorical and numerical
#print(df.head())
working_df = df[['Survived', 'Categorical_Outlier', 'Numeric_Outlier', 'Is_Outlier', 'Outlier_Reason']].copy()
print(working_df.head())
working_df.to_json('lung_cancer.json')
working_df.to_csv('lung_cancer.csv')
