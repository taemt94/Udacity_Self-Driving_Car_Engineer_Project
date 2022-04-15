import argparse
import glob
from importlib.resources import path
import os
import random
import pathlib
import numpy as np

from utils import get_module_logger


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
    
    tfrecord_paths = list(source.glob("*"))
    random.shuffle(tfrecord_paths)
    split_idx = int(0.8 * len(tfrecord_paths))
    TRAIN_PATHs = tfrecord_paths[:split_idx]
    VAL_PATHs = tfrecord_paths[split_idx:]

    TRAIN_PATHs = [path.rename(str(train_path / path.name)) for path in TRAIN_PATHs]
    VAL_PATHs = [path.rename(str(val_path / path.name)) for path in VAL_PATHs]


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