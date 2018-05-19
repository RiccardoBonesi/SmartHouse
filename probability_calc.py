import numpy

import pandas as pd

def obtain_p_adls():
    dataset = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']

    activities = []
    dataCount = []
    startProb = []
    sequence = []
    for currentDataset in dataset:
        data = pd.read_csv(currentDataset, sep="\t\t")
        activities.append(data['Activity'].unique())
        dataCount.append(data['Activity'].value_counts())
        sequence.append(data['Activity'])
        s = sum(data['Activity'].value_counts());
        norm = [float(i) / s for i in data['Activity'].value_counts()]
        startProb.append(norm)

    print("")