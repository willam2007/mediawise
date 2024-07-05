import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

file_path = r'C:\Users\warfa\Downloads\mediawise\artem\train_data.json'


df = pd.read_json(file_path)
df=pd.concat([df,pd.json_normalize(df['targetAudience'])], axis=1)
df=df.drop(['targetAudience','id'], axis=1)
print(df)
##Количество разных групп
print(df['name'].value_counts())

##Разброс возраста
plt.figure(figsize=(20, 6))
for y in range(len(df)):
  x=[df['ageFrom'].iloc[y], df['ageTo'].iloc[y]]
  plt.plot([y]*2,x, color=(31/255, 119/255, 180/255))

plt.title('Обхват по возрасту')
plt.xlabel('Группа по счету')
plt.ylabel('Разброс возрастов в группе')
plt.show()

##Разброс в точках разных групп
def plot_points(df, images_per_row = 5,  centering = False):

    num_rows = len(df) // images_per_row + int(len(df) % images_per_row != 0)
    fig, axes = plt.subplots(num_rows, images_per_row, figsize=(15, 3 * num_rows))


    for i in range(num_rows * images_per_row):
        if i < len(df):
            ax = axes.flat[i]

            g = df.iloc[i]
            points = np.array([[float(x['lat']), float(x['lon'])] for x in g['points']])
            ax.scatter(points[:, 0], points[:, 1])
            ax.axis('on')

            ax.set_title(f"{g['name']} | {g['gender']} | {g['value']} | {np.round(g['value']/len(points),2)}")

            if centering:
              #большинство точек находится в этом диапазоне
              ax.set_ylim(37.3, 37.9)
              ax.set_xlim(55.55, 55.95)
        else:
            axes.flat[i].axis('off')


    plt.tight_layout()
    plt.show()

# Группа | пол | охват | охват каждой точки в среднем
##Визуализируем географическое расположение точек
plot_points(df.iloc[:20], centering = True)