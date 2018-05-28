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
    ret = pd.DataFrame([norm],columns=dataset['Activity'].unique().tolist())
    return ret


# calcola le probabiltà di transizione
def get_trans_prob(dataset):
    nextState = []


    qwer = len(dataset.index)
    activities = dataset['Activity'].unique().tolist()
    matrix = np.zeros(len(activities))
    for state in activities:
        #INDICI IN CUI è PRESENTE STATE
        wooo = [i for i, j in enumerate(dataset['Activity'].tolist()) if j == state]
        #INDICI DELLO STATO SUCCESSIVO A STATE
        nextIndex = [x + 1 for x in wooo]
        #QWER CONTIENE IL PRIMO INDEXOUTOFBOUND
        if qwer in nextIndex:
            nextIndex.remove(qwer)
        #T CONTIENE GLI STATI SUCCESSIVI ALLO STATO CHE STO ANALIZZANDO (ES. TUTTI GLI STATI POST BREAKFAST)
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
    ret = pd.DataFrame(matrix, index=activities, columns=activities)
    print("probabilità di trasizione calcolate")
    return ret


# calcola le probabilità delle osservazioni
def get_obs_prob(dataset):
    evidence = []


    activities = dataset['Activity'].unique().tolist()
    evidenceList = dataset['Evidence'].unique().tolist()
    matrix = np.zeros(len(evidenceList))

    for state in activities:
        # INDICI IN CUI è PRESENTE STATE
        wooo = [i for i, j in enumerate(dataset['Activity'].tolist()) if j == state]
        # INDICI DELLO STATO SUCCESSIVO A STATE

        # QWER CONTIENE IL PRIMO INDEXOUTOFBOUND

        # T CONTIENE GLI STATI SUCCESSIVI ALLO STATO CHE STO ANALIZZANDO (ES. TUTTI GLI STATI POST BREAKFAST)
        T = [dataset['Evidence'].tolist()[i] for i in wooo]
        evidence.append(T)
        counter = []
        for currentEvidence in evidenceList:
            num = T.count(currentEvidence)
            counter.append(num)
            app = np.array(counter)

        norm = [float(i) / sum(app) for i in app]
        matrix = numpy.vstack([matrix, norm])

    matrix = numpy.delete(matrix, (0), axis=0)
    print("probabilità di trasizione calcolate")
    ret = pd.DataFrame(matrix, index=activities, columns=evidenceList)
    return ret

    # #data = pd.read_csv(dataset, sep="\t")
    # # per ogni attività trovare tutte le evidenze e calcolare la probabilità per ogni stato
    #
    #
    # activities = dataset['Activity'].unique().tolist()
    #
    # for activity in activities:
    #     x = dataset.loc[dataset['Activity'] == activity]
    #     s = sum(x['Evidence'].value_counts())
    #     print(s)
    #     norm = [float(i) / s for i in x['Evidence'].value_counts()]
    #     print(norm)
    # #dataCount.append(data['Activity'].value_counts())
    #
    #
    # s1 = dataset.groupby(['Activity', 'Evidence']).size()  # sommo tutte le occorrenze di attività-evidenza
    # s = sum(s1)     # numero totale di evidenze
    # norm = [float(i) / s for i in s1]
    #
    # print("probabilità delle osservazioni calcolate")
    # return norm


