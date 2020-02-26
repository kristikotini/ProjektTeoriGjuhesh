import pandas as pd
import numpy as np


def get_dataset(filename):
    dataset = pd.read_csv(filename)
    return dataset


def get_states(filename):
    dataset = pd.read_csv(filename)
    states = dataset.iloc[:, 0].values
    states = states[states != -1]
    return states

