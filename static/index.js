var geoJsonLayers = [];  // Массив для хранения ссылок на слои GeoJSON
var map;  // Глобальная переменная для хранения карты
var selectedDistrictName = null;  // Переменная для хранения выбранного района

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
    DG.marker([lat, lon]).addTo(map);
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('anketaForm');
    const checkboxes = document.querySelectorAll('input[name="options"]');
    const submitButton = document.querySelector('.firstbutton');

    form.addEventListener('submit', function(event) {
        const checkedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        if (checkedCheckboxes.length < 1 || checkedCheckboxes.length > 3) {
            event.preventDefault();
            alert('Выберите от 1 до 3 вариантов.');
        }
    });
});

function loadMarkers(data) {
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
