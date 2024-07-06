// DG.then(function () {
//     var map = DG.map('map', {
//         center: [55.752, 37.617],
//         zoom: 10
//     });

//     // Загрузка GeoJSON и добавление его на карту
//     fetch('../static/moscow.geojson')
//         .then(function(response) { return response.json(); })
//         .then(function(data) {
//             DG.geoJson(data, {
//                 onEachFeature: function (feature, layer) {
//                     layer.bindPopup('Вы выбрали: ' + feature.properties.name);

//                     // Добавить событие клика, если нужно
//                     layer.on('click', function() {
//                         //alert('Район: ' + feature.properties.name);
//                         //resetStyles();
//                         layer.setStyle({
//                             fillColor: '#3366ff', // Цвет заливки выбранного полигона
//                             fillOpacity: 0.5,    // Полупрозрачная заливка для выбранного полигона
//                             color: '#000000',    // Черный цвет границ выбранного полигона
//                             weight: 2            // Толщина границ выбранного полигона
//                         });
//                         // Можно добавить другие взаимодействия, например, обновление данных на странице
//                     });

//                     // Настройка визуального стиля полигонов
//                     layer.setStyle({
//                         fillColor: '#3366ff',
//                         fillOpacity: 0,
//                         color: '#2d3e50',
//                         weight: 2
//                     });
//                 }
//             }).addTo(map);
//         });
// });

// function resetStyles() {
//     map.eachLayer(function (layer) {
//         layer.setStyle({
//             fillColor: '#ffffff',
//             fillOpacity: 0,
//             color: '#000000',
//             weight: 2
//         });
//     });
// }


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

DG.then(function () {
    var map = DG.map('map', {
        center: [55.752, 37.617],
        zoom: 10
    });

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
                    });

                    // Добавление ссылки на слой в массив
                    geoJsonLayers.push(layer);
                }
            }).addTo(map);
        });
});
