# Создание модели
 model = Sequential()
 model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
 model.add(Dense(32, activation='relu'))
 model.add(Dense(1, activation='linear'))  # Выходной слой для регрессии 

# Компиляция модели
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

# Обучение модели
 history = model.fit(X_train, y_train, epochs=50, batch_size=10, validation_split=0.2)

# Оценка модели
 loss, mae = model.evaluate(X_test, y_test)
 print(f'Mean Absolute Error on test data: {mae}')

# Визуализация обучения
 plt.plot(history.history['loss'], label='train_loss')
 plt.plot(history.history['val_loss'], label='val_loss')
 plt.legend()
 plt.show()

# Прогнозирование
 predictions = model.predict(X_test)

# Визуализация результатов на карте города (псевдокод)
 import folium

# Создаем карту
 city_map = folium.Map(location=[55.751244, 37.618423], zoom_start=10)  # Москва как центр города

# Добавляем прогнозы на карту
 for i in range(len(X_test)):
    folium.Marker(
        location=[X_test[i][0], X_test[i][1]],  # lat, lon
        popup=f'Охват: {predictions[i][0]:.2f}',
        icon=folium.Icon(color='blue')
    ).add_to(city_map)

# Сохраняем карту в HTML
city_map.save('neyro/predicted_map.html')