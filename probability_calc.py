import numpy

import pandas as pd
from collections import Counter
import numpy as np


# calcola le probabilità iniziali
def get_start_prob(dataset):

    s = sum(dataset['Activity'].value_counts())
    print(s)
    norm = [float(i) / s for i in dataset['Activity'].value_counts()]

    print("probabilità iniziali calcolate")
    return norm


# calcola le probabiltà di transizione
def get_trans_prob(dataset):
    nextState = []


    qwer = len(dataset.index)
    activities = dataset['Activity'].unique().tolist()
    matrix = np.zeros(len(activities))
    for state in activities:
        wooo = [i for i, j in enumerate(dataset['Activity'].tolist()) if j == state]
        nextIndex = [x + 1 for x in wooo]
        if qwer in nextIndex:
            nextIndex.remove(qwer)
        T = [dataset['Activity'].tolist()[i] for i in nextIndex]
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

    #data = pd.read_csv(dataset, sep="\t")
    # per ogni attività trovare tutte le evidenze e calcolare la probabilità per ogni stato


    activities = dataset['Activity'].unique().tolist()

    for activity in activities:
        x = [j for i, j in enumerate(dataset['Evidence'].tolist()) if j == activity]
        print(x)
    #dataCount.append(data['Activity'].value_counts())


    s1 = dataset.groupby(['Activity', 'Evidence']).size()  # sommo tutte le occorrenze di attività-evidenza
    s = sum(s1)     # numero totale di evidenze
    norm = [float(i) / s for i in s1]

    print("probabilità delle osservazioni calcolate")
    return norm

