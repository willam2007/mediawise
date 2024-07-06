import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

# Загружаем обработанные данные
df = pd.read_csv('neyronka/data/processed_data.csv')

# Разделение данных на обучающую и тестовую выборки
X = df.drop(columns=['hash', 'name', 'value'])
y = df['value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)  # Получаем MSE
rmse = np.sqrt(mse)  # Вычисляем RMSE

print(f'RMSE: {rmse}')

# Сохранение модели на диск
with open('neyronka/models/linear_regression_model.pkl', 'wb') as f:
    pickle.dump(model, f)