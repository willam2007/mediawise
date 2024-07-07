var geoJsonLayers = [];  // Массив для хранения ссылок на слои GeoJSON
var map;  // Глобальная переменная для хранения карты
var selectedDistrictName = null;  // Переменная для хранения выбранного района
var markers = [];  // Массив для хранения ссылок на маркеры

function resetStyles() {
    for (var i = 0; i < geoJsonLayers.length; i++) {
        geoJsonLayers[i].setStyle({
            fillColor: '#ffffff', // Установка фона полигонов на прозрачный
            fillOpacity: 0,       // Прозрачность фона
            color: '#000000',     // Цвет границ полигонов
            weight: 2             // Толщина границ
        });
    }
}

function sendDistrictName(districtName) {
    fetch('/set-district', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ districtName: districtName })
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => console.error('Error:', error));
}

function clearMarkers() {
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
}

function validateForm() {
    document.getElementById('selectedDistrict').value = selectedDistrictName;
    return true;
}

DG.then(function () {
    map = DG.map('map', {
        center: [55.752, 37.617],
        zoom: 10
    });

    fetch('../static/input_data/moscow.geojson')
        .then(response => response.json())
        .then(data => {
            DG.geoJson(data, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup('Вы выбрали: ' + feature.properties.name);
                    layer.setStyle({
                        fillColor: '#ffffff',
                        fillOpacity: 0,
                        color: '#000000',
                        weight: 2
                    });
                    layer.on('click', function () {
                        resetStyles();
                        layer.setStyle({
                            fillColor: '#3366ff',
                            fillOpacity: 0.5,
                            color: '#000000',
                            weight: 2
                        });
                        // Отправка названия района на сервер
                        selectedDistrictName = feature.properties.name;
                        sendDistrictName(feature.properties.name);
                    });
                    geoJsonLayers.push(layer);
                }
            }).addTo(map);
            loadCoordinates();  // Вызываем загрузку координат после инициализации карты
        });
});

function loadCoordinates() {
    fetch('../static/input_data/coordinates.txt')
        .then(response => response.text())
        .then(data => loadMarkers(data))
        .catch(error => console.error('Ошибка загрузки координат:', error));
}

function addMarker(lat, lon) {
    const marker = DG.marker([lat, lon]).addTo(map);
    markers.push(marker);
}

function loadMarkers(data) {
    clearMarkers();
    console.log('Loaded data:', data);
    var lines = data.trim().split('\n');
    lines.forEach(function(line) {
        var coords = line.split(',');
        if (coords.length === 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isNaN(lat) && !isNaN(lon)) {
                addMarker(lat, lon);
            } else {
                console.error('Неверный формат координат:', line);
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Очищаем координаты при загрузке страницы
    fetch('/clear-coordinates', { method: 'POST' })
        .then(() => console.log('Coordinates cleared'))
        .catch(error => console.error('Error clearing coordinates:', error));

    const form = document.getElementById('anketaForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const checkboxes = document.querySelectorAll('input[name="options"]');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const options = formData.getAll('options').join('');
        formData.set('options', options);

        formData.set('selectedDistrict', selectedDistrictName);

        fetch('/submit', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = '';
            clearMarkers();  // Очищаем существующие маркеры
            data.best_points.forEach(point => {
                const resultItem = document.createElement('div');
                resultItem.classList.add('result-item');

                resultItem.innerHTML = `
                    <h3>Координаты: ${point.lat}, ${point.lon}</h3>
                    <p>Возраст от: ${data.age_from}, до: ${data.age_to}</p>
                    <p>Пол: ${data.sex_status}</p>
                    <p>Количество билбордов: ${data.buildboard_number}</p>
                    <p>Доход: ${data.selected_options}</p>
                    <p>Район: ${data.selected_district}</p>
                    <p>Предсказанная эффективность: ${point.predicted_value}</p>
                `;
                resultsContainer.appendChild(resultItem);
                
                // Добавление меток на карту
                addMarker(point.lat, point.lon);
            });
            resultsContainer.classList.remove('typewriter'); // Убираем класс для перезапуска анимации
            void resultsContainer.offsetWidth; // Триггер для перезапуска анимации
            resultsContainer.classList.add('typewriter');
        })
        .catch(error => {
            console.error('Ошибка:', error);
            resultsContainer.textContent = 'Произошла ошибка при отправке данных.';
        });
    });
});
