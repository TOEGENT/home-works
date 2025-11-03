import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error 
import numpy as np
import matplotlib
df=pd.read_csv('cars_train.csv')

def clear_df(df):
   df['Engine'] = df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Distance'] = df['Distance'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Wheel'] = df['Wheel'].map({'Left wheel':0,'Right-hand drive':1})
   df['Transmission'] = (df['Transmission'] == 'Manual').astype(int)
   df['Drive'] = (df['Drive'] == '4x4').astype(int)

   return df
df = clear_df(df).drop(columns=['ID'])
print(df.dtypes)
numeric_df = df.select_dtypes(include='number')
numeric_df = numeric_df.dropna()
X = numeric_df.drop('Price', axis=1)
y = numeric_df['Price']
total=[]
"""
for i in range(10):
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=i)
   model = GradientBoostingRegressor(random_state=i,max_depth=5,subsample=0.8,learning_rate=0.05,n_estimators=500)
   model.fit(X_train, y_train)


   # Предсказание
   y_pred = model.predict(X_test)
   MAE = mean_absolute_error(y_test, y_pred)
   MAPE = mean_absolute_percentage_error(y_test, y_pred)
   total.append(MAPE)
print(sum(total)/len(total),sorted(total)[len(total)//2])
"""
"""
df_submit.to_csv('submit.csv', index = False)
df_submit.head(3)

import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error 

df_submit=pd.read_csv('submit.csv')
df_test=pd.read_csv('cars_test_full.csv')


df_merged = pd.merge(df_submit, df_test, on='ID', how='left').drop_duplicates()

y_true = df_merged['Price']
y_pred = df_merged['Predict']

MAE = mean_absolute_error(y_true, y_pred)
MAPE = mean_absolute_percentage_error(y_true, y_pred)  

print("MAE:", MAE)
print("MAPE, %:", MAPE )
"""