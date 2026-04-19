import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
df = pd.read_csv('./cardio_train.csv')
df.drop(columns='id')
df['weight'] = df['weight'].astype('int')
df['Outlier_Reason'] = ''
df['Is_Outlier'] = False
print(df.info())
numeric_cols = df.select_dtypes(include='number').columns
for group_value in ['0','1']: #for the answers of no and yes
    group = df[df['cardio']==group_value] #the group of this iteration is the group that is either yes or no
    for col in numeric_cols: #for the numeric columns
        z = np.abs(stats.zscore(group[col])) #get the z score of all the nos for that column and all the yes's for that column
        outlier_mask = (z>3) #a boolean series of which values have a z score (deviation) that is greater than 3, which makes it an outlier
        outlier_index = group.index[outlier_mask]
        df.loc[outlier_index, 'Is_Outlier'] = True #the indeces of these values, for that group, is set to true
        df.loc[outlier_index, 'Outlier_Reason'] += (col + '=' + df.loc[outlier_index,col].astype(str) + '; ')
print(df.head())
df.to_json('cardio_outliers.json')
df.to_csv('cardio_outliers.csv')