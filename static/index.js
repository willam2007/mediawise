var geoJsonLayers = [];  // Массив для хранения ссылок на слои GeoJSON

// Функция, которая сбрасывает стили для всех слоев полигонов
function resetStyles() {
    // Итерация по массиву слоёв полигонов
    for (var i = 0; i < geoJsonLayers.length; i++) {
        geoJsonLayers[i].setStyle({
            fillColor: '#ffffff', // установка фона полигонов на прозрачный
            fillOpacity: 0,       // прозрачность фона
            color: '#000000',     // цвет границ полигонов
            weight: 2             // толщина границ
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

DG.then(function () {
    var map = DG.map('map', {
        center: [55.752, 37.617],
        zoom: 10
    });


    DG.marker([55.750419, 37.542603]).addTo(map);

    // Загрузка и добавление GeoJSON на карту
    fetch('../static/moscow.geojson')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            DG.geoJson(data, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup('Вы выбрали: ' + feature.properties.name);
                    // Установка начального стиля для полигонов
                    layer.setStyle({
                        fillColor: '#ffffff',
                        fillOpacity: 0,
                        color: '#000000',
                        weight: 2
                    });

                    // Обработчик клика по полигону
                    layer.on('click', function () {
                        resetStyles();  // Сброс стилей всех полигонов
                        layer.setStyle({  // Применение нового стиля для выбранного полигона
                            fillColor: '#3366ff',
                            fillOpacity: 0.5,
                            color: '#000000',
                            weight: 2
                        });
                        // Отправка названия района на сервер
                        sendDistrictName(feature.properties.name);
                    });

                    // Добавление ссылки на слой в массив
                    geoJsonLayers.push(layer);
                }
            }).addTo(map);
        });
});