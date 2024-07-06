import json
from shapely.geometry import shape, Point
from operator import itemgetter

def filter_points_by_district(data, district_polygon):
    filtered_points = []
    seen_points = {}  # Словарь для отслеживания уже встреченных точек

    for entry in data:
        for point in entry['points']:
            point_obj = Point(point['lon'], point['lat'])
            if district_polygon.contains(point_obj):
                point_key = (point['lat'], point['lon'])
                if point_key not in seen_points:
                    seen_points[point_key] = {
                        "hash": entry['hash'],
                        "lat": point['lat'],
                        "lon": point['lon'],
                        "azimuth": point['azimuth'],
                        "value": entry['value'],
                        "gender": entry['targetAudience']['gender'],
                        "ageFrom": entry['targetAudience']['ageFrom'],
                        "ageTo": entry['targetAudience']['ageTo'],
                        "income": entry['targetAudience']['income']
                    }
                else:
                    if entry['value'] > seen_points[point_key]['value']:
                        seen_points[point_key] = {
                            "hash": entry['hash'],
                            "lat": point['lat'],
                            "lon": point['lon'],
                            "azimuth": point['azimuth'],
                            "value": entry['value'],
                            "gender": entry['targetAudience']['gender'],
                            "ageFrom": entry['targetAudience']['ageFrom'],
                            "ageTo": entry['targetAudience']['ageTo'],
                            "income": entry['targetAudience']['income']
                        }

    filtered_points = list(seen_points.values())
    return filtered_points

def load_district_polygons(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        district_data = json.load(file)
    district_polygons = {}
    for feature in district_data['features']:
        district_name = feature['properties']['name']
        polygon = shape(feature['geometry'])
        district_polygons[district_name] = polygon
    return district_polygons

def find_district_for_point(point, district_polygons):
    point_obj = Point(point['lon'], point['lat'])
    for district_name, polygon in district_polygons.items():
        if polygon.contains(point_obj):
            return district_name
    return None

def fileforkolya(district_name):
    # Чтение данных из файла
    with open('neyron/train_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Чтение данных районов
    district_polygons = load_district_polygons('neyron/moscow.geojson')
    
    # Проверка существования района
    if district_name not in district_polygons:
        print(f"Район '{district_name}' не найден.")
        return

    district_polygon = district_polygons[district_name]
    filtered_points = filter_points_by_district(data, district_polygon)
    
    # Сортировка точек по убыванию value
    filtered_points_sorted = sorted(filtered_points, key=itemgetter('value'), reverse=True)

    # Запись результата в новый файл
    with open('neyron/filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_points_sorted, file, ensure_ascii=False, indent=4)

    # Вывод результата
    print(district_name)
    for point in filtered_points_sorted:
        print(f"{point['lat']},{point['lon']}")


