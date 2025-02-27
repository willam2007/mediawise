import json
from shapely.geometry import shape, Point


# Загрузка данных районов
with open('./static/input_data/moscow.geojson', 'r') as f:
    districts = json.load(f)

# Загрузка выбранного района из файла
with open('./static/district_choise/district_name.txt', 'r') as file:
    district_name = file.read().strip()
    print(district_name)

polygon = None
for feature in districts['features']:
    if feature['properties']['name'] == district_name:
        print('popa')
        polygon = shape(feature['geometry'])
        print(polygon.bounds)
        break

if polygon is None:
    raise ValueError("Район не найден")

# Загрузка данных о рекламе
with open('./static/input_data/train_data.json', 'r') as f:
    ads = json.load(f)

# Фильтрация данных, включение только тех точек, которые находятся внутри полигона
filtered_ads = []
for ad in ads:
    valid_points = []
    for point in ad['points']:
        if polygon.contains(Point(float(point['lon']), float(point['lat']))):
            print('pisa')
            valid_points.append(point)
    if valid_points:
        ad['points'] = valid_points
        filtered_ads.append(ad)

# Сохранение отфильтрованных данных
with open('./static/district_choise/filtered_train_data.json', 'w') as f:
    json.dump(filtered_ads, f, indent=4)
