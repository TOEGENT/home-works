import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error 
import numpy as np
import matplotlib
from sklearn.pipeline import  Pipeline
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('cars_train.csv')


plt.figure(figsize=(10,5))
sns.histplot(df["Distance"],bins=50,kde=True)
plt.title("Распределение пробега")
plt.xlabel("Пробег в км")
plt.ylabel("Количество автомобилей")
#plt.show()

plt.figure(figsize=(8,4))
sns.boxplot(x=df["Distance"])
plt.title("Boxplot пробега")
plt.xlabel("Пробег в км")
#plt.show()


def clear_df_train(df):
   df['Engine'] = df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Distance'] = df['Distance'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Wheel'] = df['Wheel'].map({'Left wheel': 0, 'Right-hand drive': 1})
   df['Transmission'] = (df['Transmission'] == 'Manual').astype(int)
   df['Drive'] = (df['Drive'] == '4x4').astype(int)
   df = df[(df["Distance"] >= 0) & (df["Distance"] <= 999999)]
   df = df[(df["Engine"] >= 0.5) & (df["Engine"] <= 10)]
   df = df[(df["Price"] > 50) & (df["Price"] < 500000)]
   return df


def clear_df_test(df):
   df['Engine'] = df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Distance'] = df['Distance'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
   df['Wheel'] = df['Wheel'].map({'Left wheel': 0, 'Right-hand drive': 1})
   df['Transmission'] = (df['Transmission'] == 'Manual').astype(int)
   df['Drive'] = (df['Drive'] == '4x4').astype(int)

   return df
df = clear_df_train(df).drop(columns=['ID'])

X =df.drop('Price', axis=1)
y = np.log1p(df['Price'])
df=df.drop("Price",axis=1)
numerical = df.select_dtypes(include="number").columns.tolist()
categorical = df.select_dtypes(include=["object","string"]).columns.tolist()

preprocessor = ColumnTransformer(
   transformers=[
      ("num",
       Pipeline([
         ("imputer",SimpleImputer(strategy="median")),
         ("scaler",RobustScaler())
      ]),numerical),
      ("cat",OneHotEncoder(drop="first",handle_unknown="ignore",sparse_output=False),categorical)
   ],
   remainder="drop"
)


"""
print(df)
categorical_cols=df.select_dtypes(include=["object","string"]).columns.tolist()
print("categorial_features",categorical_cols)
for col in categorical_cols:
   n_unique=df[col].nunique()
   print(f"{col}:{n_unique}")
print(df.Model.sample(10).tolist())
print(df[["Make","Model"]].value_counts().head(20))

for make in df["Make"].unique():
   models=df[df["Make"]==make]["Model"].value_counts().head(10)
   print(f"\n{make}:")
"""

total=[]
total2=[]

# ОТБОР ПРИЗНАКОВ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
X_train_enc = preprocessor.fit_transform(X_train)
X_test_enc = preprocessor.transform(X_test)

feature_names = preprocessor.get_feature_names_out()

model = GradientBoostingRegressor(random_state=42, max_depth=5, subsample=0.5, learning_rate=0.1, n_estimators=100)
model.fit(X_train_enc, y_train)

feat_imp = pd.DataFrame({
   "feature": feature_names,
   "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

selected_features = feat_imp[feat_imp["importance"] > 0]["feature"].values
selected_indices = [list(feature_names).index(f) for f in selected_features]

for i in range(1):

   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
   X_train_enc=preprocessor.transform(X_train)
   X_test_enc = preprocessor.transform(X_test)
   feature_names=preprocessor.get_feature_names_out()
   selected_mask=np.isin(feature_names,selected_features)
   X_train_final=X_train_enc[:,selected_mask]
   X_test_final=X_test_enc[:,selected_mask]

   #print("Форма обучающей выборки после OHE:", X_train_final.shape)
   X_train_df = pd.DataFrame(X_train_final,columns=selected_features)
   X_test_df=pd.DataFrame(X_test_final,columns=selected_features)
   #print(X_train_df)
   y_train_real = np.expm1(y_train)
   y_test_real=np.expm1(y_test)

   model = GradientBoostingRegressor(random_state=42,max_depth=15,subsample=0.3,learning_rate=0.05,n_estimators=2000)
   model.fit(X_train_final, y_train)
   y_pred_train=np.expm1(model.predict(X_train_final))
   y_pred_test=np.expm1(model.predict(X_test_final))
   MAE = mean_absolute_error(y_train_real, y_pred_train)
   MAPE = mean_absolute_percentage_error(y_train_real, y_pred_train)


   MAE = mean_absolute_error(y_test_real, y_pred_test)
   MAPE = mean_absolute_percentage_error(y_test_real, y_pred_test)
   print("MAE",MAE)
   print(f"MAPE: {MAPE}%")

   total.append(MAPE)
   total2.append(MAE)
print(sum(total)/len(total),sorted(total)[len(total)//2])
print(sum(total2)/len(total2),sorted(total2)[len(total2)//2])

df_test = pd.read_csv('cars_test.csv')
df_test = clear_df_test(df_test)
df_test = df_test.dropna().drop_duplicates()
print(df_test.shape)
# Преобразование через preprocessor
X_test_enc = preprocessor.transform(df_test[X.columns])
feature_names = preprocessor.get_feature_names_out()
selected_mask = np.isin(feature_names, selected_features)
X_test_final = X_test_enc[:, selected_mask]

# Предсказание
y_pred = np.expm1(model.predict(X_test_final))

# Сборка файла для отправки
df_submit = df_test[['ID']].copy()
df_submit['Predict'] = y_pred
df_submit.to_csv('submit.csv', index=False)
print("submit",df_submit.shape)
print(df_submit.head(3))