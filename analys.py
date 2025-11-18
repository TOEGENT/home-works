# pip install catboost==1.1.1 scikit-learn pandas numpy
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# ---- Загрузка и очистка (модифицированная) ----
def clear_df(df):
    # извлечь числа из строк
    if 'Engine' in df.columns:
        df['Engine'] = df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
    if 'Distance' in df.columns:
        df['Distance'] = df['Distance'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
    # wheel/Transmission/Drive — аккуратно: возможны разные текстовые значения
    if 'Wheel' in df.columns:
        df['Wheel'] = df['Wheel'].astype(str).replace({
            'Left wheel': 'left',
            'Right-hand drive': 'right',
            'Left-hand drive': 'left',
            'Right wheel': 'right'
        }).where(lambda x: x != 'nan', other=np.nan)
    if 'Transmission' in df.columns:
        df['Transmission'] = df['Transmission'].astype(str)
    if 'Drive' in df.columns:
        df['Drive'] = df['Drive'].astype(str)
    return df

# ---- Чтение данных ----
train = pd.read_csv('cars_train.csv')
test  = pd.read_csv('cars_test.csv')

train = clear_df(train)
test  = clear_df(test)

# Сохраняем ID отдельно
train_id = train.get('ID')
test_id  = test.get('ID')

# Не дропаем na полностью — пометим и обработаем
# Список признаков, которые мы хотим использовать (включая категориальные)
# Берём все колонки, кроме целевой и ID
exclude = {'ID', 'Price'}
features = [c for c in train.columns if c not in exclude]

# Обнаружим категориальные признаки автоматически (object / category), но
# сохраняем числовые, даже если есть пропуски (CatBoost умеет с ними работать)
cat_features = [c for c in features if train[c].dtype == 'object' or train[c].dtype.name == 'category']

# Приведём категориальные столбцы к типу 'category' (рекомендуется)
for c in cat_features:
    train[c] = train[c].astype('category')
    test[c]  = test[c].astype('category')

# Заполнение: CatBoost поддерживает NaN, но для стабильности можно заполнить часть чисел медианой
num_cols = [c for c in features if c not in cat_features]
for c in num_cols:
    median = train[c].median()
    train[c] = train[c].fillna(median)
    # Если в тесте появится новая колонка с NaN — тоже заполним медианой из train
    if c in test.columns:
        test[c]  = test[c].fillna(median)

# Обработка категориальных NaN — оставляем как NaN (CatBoost умеет) или преобразуем в строку 'missing'
for c in cat_features:
    train[c] = train[c].cat.add_categories(['__missing__']).fillna('__missing__')
    if c in test.columns:
        test[c]  = test[c].cat.add_categories(['__missing__']).fillna('__missing__')

# ---- Целевая трансформация (рекомендуется при сильном скошенном Price) ----
y = train['Price'].values
# лог-трансформируем для стабильности обучения, потом инвертируем при оценке
y_log = np.log1p(y)

X = train[features].copy()
X_test_final = test[features].copy()

# ---- Разделение на train / val для мониторинга ----
X_tr, X_val, y_tr, y_val = train_test_split(X, y_log, test_size=0.15, random_state=42)

# ---- Подготовка Pool'ов CatBoost ----
train_pool = Pool(X_tr, label=y_tr, cat_features=cat_features)
val_pool   = Pool(X_val, label=y_val, cat_features=cat_features)

# ---- Модель CatBoost (базовый конфиг, можно тюнить) ----
model = CatBoostRegressor(
    iterations=3000,
    learning_rate=0.03,
    depth=8,
    loss_function='MAE',           # оптимизируем под MAE
    eval_metric='MAE',
    random_seed=42,
    early_stopping_rounds=100,
    task_type='CPU',               # или 'GPU' если доступна
    verbose=200
)

model.fit(train_pool, eval_set=val_pool, use_best_model=True)

# ---- Оценка: предсказание и обратное преобразование ----
y_val_pred_log = model.predict(val_pool)
y_val_pred = np.expm1(y_val_pred_log)         # обратный log1p
y_val_true = np.expm1(y_val)                  # т.к. y_val — в логах

mae = mean_absolute_error(y_val_true, y_val_pred)
mape = mean_absolute_percentage_error(y_val_true, y_val_pred)
print("Validation MAE:", mae)
print("Validation MAPE:", mape)

# ---- Предсказание для теста (с учётом возможного несовпадения колонок) ----
# Убедимся, что тест содержит все признаки в том же порядке
missing_cols = [c for c in features if c not in X_test_final.columns]
for c in missing_cols:
    X_test_final[c] = 0  # или медиана, или '__missing__' для категорий

X_test_final = X_test_final[features]
test_pool = Pool(X_test_final, cat_features=cat_features)
test_pred_log = model.predict(test_pool)
test_pred = np.expm1(test_pred_log)

submission = pd.DataFrame({'ID': test_id, 'Predict': test_pred})
submission.to_csv('submit_catboost.csv', index=False)

# ---- Полезные инструменты после обучения ----
# feature importance
fi = model.get_feature_importance(prettified=True)
print(fi.head(20))
# можно сохранить модель
model.save_model('catboost_model.cbm')
