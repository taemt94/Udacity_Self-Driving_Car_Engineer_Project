import matplotlib
# %matplotlib inline
from utils import get_dataset, parse_frame
import pathlib
import matplotlib.pyplot as plt
from waymo_open_dataset import dataset_pb2 as open_dataset
import tensorflow as tf
base_path = pathlib.Path().cwd() / 'data' / 'training_and_validation'
tf_record_path = [str(path) for path in list(base_path.glob("*"))][0]
save_path = pathlib.Path().cwd() / 'EDA_result'
dataset = get_dataset(tf_record_path)
filenames = []
file_cnt = 0

cnt = 0
for batch in dataset.take(20000):
    print(batch['filename'])
    pass
# for ds in dataset:
#     cnt += 1
#     print(f"{cnt} : {ds['filename']}")

# dataset_iter = iter(dataset)
# while True:
#     batch = dataset_iter.next()
#     # print(batch.keys())
#     filename = batch['filename']
#     print(filename)
#     # if filename not in filenames:
#     #     filenames.append(filename)
#     print(filename)
#     # print(batch.keys())
#     # print(batch['image'].shape)
#     # print(batch['filename'])
    
#     # print(type(batch['filename']))
#     # print(batch['groundtruth_classes'])
    # pass