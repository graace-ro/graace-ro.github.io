import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
df = pd.read_csv("./lung_cancer_data/lung_cancer_dataset.csv")
numeric_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(include="str").columns
#print(numeric_cols)
#print(categorical_cols)