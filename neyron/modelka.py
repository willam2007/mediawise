import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.preprocessing import MinMaxScaler

# Загрузка данных
df = pd.read_csv('formatted_data.csv')

# Нормализация целевой переменной
scaler = MinMaxScaler()
df['value'] = scaler.fit_transform(df[['value']])

# Подготовка данных
X = df[['gender', 'age_from', 'age_to', 'income', 'lat', 'lon', 'azimuth']]
y = df['value']

# Преобразование категориальных признаков в числовые
X = pd.get_dummies(X, columns=['gender', 'income'])

# Разделение данных на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Определение параметров для поиска
param_grid_gb = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}

# Обучение и оптимизация модели GradientBoostingRegressor
gb = GradientBoostingRegressor(random_state=42)
grid_search_gb = GridSearchCV(estimator=gb, param_grid=param_grid_gb, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_gb.fit(X_train, y_train)

# Выбор лучшей модели и предсказания
best_gb = grid_search_gb.best_estimator_

# Предсказания на тестовой выборке
y_pred_gb = best_gb.predict(X_test)

# Денормализация предсказаний
y_pred_gb = scaler.inverse_transform(y_pred_gb.reshape(-1, 1)).flatten()
y_test = scaler.inverse_transform(y_test.values.reshape(-1, 1)).flatten()

rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))
custom_metric_gb = max(1 - rmse_gb / 30, 0) ** 4

print(f'GradientBoosting RMSE: {rmse_gb}')
print(f'GradientBoosting Custom Metric: {custom_metric_gb}')

# Сохранение модели
joblib.dump(best_gb, 'best_gb_model.pkl')
joblib.dump(scaler, 'scaler.pkl')