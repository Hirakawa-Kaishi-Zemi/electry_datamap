#電力会社ごとの区域
import matplotlib.pyplot as plt
import japanize_matplotlib
from japanmap import picture
import pandas as pd

dict_area= pd.read_csv('csv/areamap.csv', index_col=0).to_dict()

color =  dict_area['カラー']


plt.rcParams['figure.figsize'] = (8, 8)

plt.imshow(picture(color))
plt.title('色別電力会社の区域')

plt.savefig('colormap.png')
