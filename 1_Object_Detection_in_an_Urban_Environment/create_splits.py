import argparse
import random
import pathlib

from utils import get_module_logger, get_dataset


def count_class(_dataset, _sample_num, _class_cnt_dict):
    
    for batch in _dataset.take(_sample_num):
        gt_classes = batch['groundtruth_classes']
        for gt_cls in gt_classes.numpy():
            _class_cnt_dict[gt_cls] += 1
    return _class_cnt_dict


def check_objects_num(paths):
    print("[INFO] Check data validity... This might take some times.")
    data_mode = paths[0].parent.name
    label_map = {1: 'car', 2: 'pedestrian', 4: 'cyclist'}
    class_cnt_dict = {1: 0, 2: 0, 4: 0}
    sample_num = 10000
    for i, path in enumerate(paths):
        dataset = get_dataset(str(path))
        class_cnt_dict = count_class(dataset, sample_num, class_cnt_dict)
    print(f"Total objects number of {data_mode} data :")
    for cls_idx, num in class_cnt_dict.items():
        print(f"{label_map[cls_idx]} : {num}")

    if class_cnt_dict[2] > 0 and class_cnt_dict[4] > 0:
        return True
    else:
        return False


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # TODO: Implement function
    source = pathlib.Path(source)
    destination_paths = list(pathlib.Path(destination).glob("*"))
    train_path = [path for path in destination_paths if "train" in str(path) and 'val' not in str(path)][0]
    val_path = [path for path in destination_paths if "val" in str(path) and 'train' not in str(path)][0]
    train_path.mkdir(exist_ok=True, parents=True)
    val_path.mkdir(exist_ok=True, parents=True)
    
    tfrecord_paths = list(source.glob("*"))
    
    while True:
        random.shuffle(tfrecord_paths)

        ### Split data into train and validation by the ratio of 8 : 2
        split_idx = int(0.8 * len(tfrecord_paths))
        TRAIN_PATHs = tfrecord_paths[:split_idx]
        VAL_PATHs = tfrecord_paths[split_idx:]

        ### Move .tfrecord to ./data/train and ./data/val
        NEW_TRAIN_PATHs = [path.rename(str(train_path / path.name)) for path in TRAIN_PATHs]
        NEW_VAL_PATHs = [path.rename(str(val_path / path.name)) for path in VAL_PATHs]

        ### Count the number of objects and check the validity of this split.
        ### If .tfrecord files in ./data/val do not contain any pedestrian or cyclist objects,
        ### data splitting needs to be done again by while loop
        train_data_valid = check_objects_num(NEW_TRAIN_PATHs)
        val_data_valid = check_objects_num(NEW_VAL_PATHs)
        if train_data_valid and val_data_valid:
            print("Data split is valid.")
            break
        else:
            ### If data are not valid, move all data to source and repeat splitting data.
            print("Data split is not valid. Repeat splitting again...")
            for path in NEW_TRAIN_PATHs:
                path.rename(str(source / path.name))
            for path in NEW_VAL_PATHs:
                path.rename(str(source / path.name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)