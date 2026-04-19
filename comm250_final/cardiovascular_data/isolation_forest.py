from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import shap

# Load your dataset
df = pd.read_csv("cardio_train.csv")
df = df.drop(columns=['id', 'age'])

# Focus on the cardio = 1 group
df_disease = df[df['cardio'] == 1]
df_healthy = df[df['cardio'] == 0]

def outler_finder_forest(group):
    # Select numeric columns (binary + continuous)
    X = group.select_dtypes(include=[np.number])
    iso = IsolationForest(n_estimators=300, contamination=0.02, random_state=42, bootstrap=False)
    #n_estimators is the number of the trees, more trees means more stable anomaly scores
    #contaimination tells the model that about 2% of this gorup are outliers
    #random_state=42 ensures reproducability
    iso.fit(X) #model learns the structure of the cardio group
    labels = iso.predict(X) #-1 is an outlier, 1 is normal
    scores = iso.decision_function(X) #lower score means more anamolous
    df.loc[group.index, "IF_Label"] = labels
    df.loc[group.index, "IF_AnomalyScore"] = scores
    outliers = df.loc[(df['cardio']==1) & (df['IF_Label']==-1)]
    # Compute medians for cardio=1 group
    medians = X.median()
    # Only look at outliers
    outlier_idx = df.loc[(df['cardio']==1) & (df['IF_Label']==-1)].index

outler_finder_forest(df_disease)
outler_finder_forest(df_healthy)
df_outliers = df[df['IF_Label']==-1]
print(df_outliers.info())
print(df_outliers)
#print(outliers)
#df_outliers.to_csv('cardio_outliers.csv')