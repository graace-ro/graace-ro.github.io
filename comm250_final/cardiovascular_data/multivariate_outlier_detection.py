import pandas as pd 
import numpy as np
from scipy.stats import chi2
#THIS DOESN'T WORK WITH BINARY VARIABLES BECAUSE THERE'S NOT ENOUGH VARIANCE. BEST WITH CONTINUOUS
df = pd.read_csv("cardio_train.csv")
df = df.drop(columns=['id', 'age'])
df_healthy = df[df['cardio']==0]
df_disease = df[df['cardio']==1]

def mahalanobis_outliers(group, top_k=3):
    numeric = group.select_dtypes(include=[np.number]) #this only works with continuous numeric values
    cols = numeric.columns #need the names for later
    #standardize the data
    X = (numeric-numeric.mean())/numeric.std() #each feature is given mean 0 and std 1. this will reduce singularity problems with the matrix later and prevent large-scale variables from dominating the covariance. X is now an nxd matrix where n is the number of people in the subgroup and d is the number of variables
    mu = X.mean().values #vector of length d (one mean per feautre)
    cov = np.cov(X.values, rowvar=False) #dxd covariance matrix. the rows are the samples and the columns are the variables
    cov_inv = np.linalg.pinv(cov) #the pseudoinverse of the above covariance matrix. only inverts non-zero eigenvalues
    diff = X.values - mu #for each row, subtract the mean vector. the shape is still nxd
    md = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1)) #this is doing the multivariate equation. so it's the difference transposed multiplied by the inverse of the covariance matrix, then multiply by the difference again. then square root the whole thing. the shape is just n
    #computing the chi-square threshold
    threshold = np.sqrt(chi2.ppf(0.999, df=X.shape[1]))
    is_outlier = md > threshold
    #the mahalanobis distance squared follows a chi-square distribution with d degrees of freedom (the number of columns), ppf(0.999) is the 99.9th percentile. if a point's distance exceeds this threshold then it's a multivariate outlier
    #compute per-feature contribution
    diag_inv = np.diag(cov_inv) #extracts the diagonal of the convariance inverse matrix. each diagonal element weights how important that feature is in the multivariate geometry
    contrib = (diff**2) * diag_inv #difference squared times the diagonals for each feature. this gives a per-feature contribution to the distances. shape is nxd
    reasons=[]
    for row_idx in range(len(X)):
        row_contrib = contrib[row_idx] 
        top_idx = np.argsort(row_contrib)[-top_k:][::-1] ##for each row sort contributions from largest to smallest top_k will pick the top 3 variables
        reason_parts = []
        for i in top_idx: #for each top contributing feature
            col=cols[i] #get the column name
            val = numeric.iloc[row_idx,i] #get the original unstandardized value
            reason_parts.append(f"{col}={val}") #store is at feature=value
        reasons.append(", ".join(reason_parts))
    return md, is_outlier, reasons
    


# Apply to cardio = 1 group
md_d, out_d, reason_d = mahalanobis_outliers(df_disease,top_k=3)

df.loc[df_disease.index, "Mahalanobis_D"] = md_d
df.loc[df_disease.index, "Is_Outlier"] = out_d
df.loc[df_disease.index, 'Outlier_Reason'] = reason_d
print(df)