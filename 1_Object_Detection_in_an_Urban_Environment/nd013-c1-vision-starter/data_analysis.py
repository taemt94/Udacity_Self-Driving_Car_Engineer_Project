import matplotlib


# %matplotlib inline
from utils import get_dataset, parse_frame
import pathlib
import matplotlib.pyplot as plt
from waymo_open_dataset import dataset_pb2 as open_dataset

x = range(10)
y = range(10, 20)

plt.plot(x, y)
plt.show()
plt.close()