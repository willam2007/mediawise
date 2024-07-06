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
    function saveAndDownloadDistrict(districtName) {
        // Удаление файла, если он уже существует
        deleteFileIfExists('selectedDistrict.json', function() {
            // Продолжаем с созданием нового файла
            const data = { district: districtName };
            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'selectedDistrict.json';
            a.click();
            URL.revokeObjectURL(url);
        });
    }
    
    // Функция для удаления файла, если он существует
    function deleteFileIfExists(filename, callback) {
        const xhr = new XMLHttpRequest();
        xhr.open('HEAD', filename, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Файл существует, удаляем его
                    const xhrDelete = new XMLHttpRequest();
                    xhrDelete.open('DELETE', filename, true);
                    xhrDelete.onreadystatechange = function() {
                        if (xhrDelete.readyState === 4 && xhrDelete.status === 200) {
                            // Файл успешно удален
                            console.log('File deleted:', filename);
                            callback(); // Вызываем функцию обратного вызова
                        }
                    };
                    xhrDelete.send();
                } else {
                    // Файл не существует или произошла ошибка при проверке, продолжаем без удаления
                    console.log('File not found or error:', filename);
                    callback(); // Вызываем функцию обратного вызова в любом случае
                }
            }
        };
        xhr.send();
    }
    
    // Измените обработчик клика по полигону
    fetch('../static/moscow.geojson')
        .then(function(response) { return response.json(); })
        .then(function(data) {
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
    
                        saveAndDownloadDistrict(feature.properties.name);
                    });
    
                    geoJsonLayers.push(layer);
                }
            }).addTo(map);
        });
});
