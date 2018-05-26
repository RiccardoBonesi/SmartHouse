import numpy

import pandas as pd
from collections import Counter
import numpy as np


# calcola le probabilità iniziali
def get_start_prob(dataset):
    activities = []
    dataCount = []
    sequence = []
    data = pd.read_csv(dataset, sep="\t\t")
    # activities.append(data['Activity'].unique())
    # dataCount.append(data['Activity'].value_counts())
    # sequence.append(data['Activity'])
    s = sum(data['Activity'].value_counts())
    print(s)
    norm = [float(i) / s for i in data['Activity'].value_counts()]

    print("probabilità iniziali calcolate")
    return norm


# calcola le probabiltà di transizione
def get_trans_prob(dataset):
    nextState = []

    data = pd.read_csv(dataset, sep="\t\t")
    qwer = len(data.index)
    activities = data['Activity'].unique().tolist()
    matrix = np.zeros(len(activities))
    #assss = data['Activity'].tolist()
    for state in activities:
        wooo = [i for i, j in enumerate(data['Activity'].tolist()) if j == state]
        nextIndex = [x + 1 for x in wooo]
        if qwer in nextIndex:
            nextIndex.remove(qwer)
        T = [data['Activity'].tolist()[i] for i in nextIndex]
        nextState.append(T)
        counter = []
        for secState in activities:
            num = 0
            num = T.count(secState)
            counter.append(num)
            app = np.array(counter)

        norm = [float(i) / sum(app) for i in app]
        matrix = numpy.vstack([matrix, norm])

    matrix = numpy.delete(matrix, (0), axis=0)
    print("probabilità di trasizione calcolate")
    return matrix


# calcola le probabilità delle osservazioni
def get_obs_prob(dataset):
    data = pd.read_csv(dataset, sep="\t")

    s1 = data.groupby(['Location', 'Type']).size()  # sommo tutte le occorrenze di attività-evidenza
    s = sum(s1)     # numero totale di evidenze
    norm = [float(i) / s for i in s1]

    print("probabilità delle osservazioni calcolate")
    return norm

