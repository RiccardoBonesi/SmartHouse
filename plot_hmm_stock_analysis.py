from __future__ import division
import numpy as np
from datset_utils import *
from probability_calc import *
from hmm import *
from hmmlearn import hmm









if __name__ == '__main__':

    # DATASET
    datasetList = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']
    sensorList = ['Dataset/OrdonezA_Sensors.txt', 'Dataset/OrdonezB_Sensors.txt']

    for dataset in datasetList:
        mergedDataset = merge_dataset(dataset, sensorList[datasetList.index(dataset)])

        # CREO TRAIN E TEST SET
        if dataset == 'Dataset/OrdonezA_ADLs.txt':
            trainIndex = range(0, 367)
            testIndex = range(367, len(mergedDataset.index))
            train = mergedDataset.loc[trainIndex, :]
            test = mergedDataset.loc[testIndex, :]
        else:
            trainIndex = range(0, 2079)
            testIndex = range(2079, len(mergedDataset.index))
            train = mergedDataset.loc[trainIndex, :]
            test = mergedDataset.loc[testIndex, :]
        startProb = get_start_prob(train)
        transProb = get_trans_prob(train)
        obsProb = get_obs_prob(train) # passare mergedDataset

        # CONVERTO OSSERVAZIONI IN NUMERI
        evidences = mergedDataset['Evidence'].unique().tolist()
        emissions = test['Evidence'].values.flatten()
        for idx, val in enumerate(emissions):
            emissions[idx] = evidences.index(val)


        # CONVERTO GLI STATI IN NUMERI
        activities = mergedDataset['Activity'].unique().tolist()
        giusti = test['Activity'].values.flatten()
        for idx, val in enumerate(giusti):
            giusti[idx] = activities.index(val)

        states = ["Rainy", "Sunny"]
        n_states = len(activities)

        observations = ["walk", "shop", "clean"]
        n_observations = len(emissions)

        start_probability = np.array([0.6, 0.4])

        transition_probability = np.array([
            [0.7, 0.3],
            [0.4, 0.6]
        ])

        emission_probability = np.array([
            [0.1, 0.4, 0.5],
            [0.6, 0.3, 0.1]
        ])
        banana = np.array(obsProb.values)
        model = hmm.GaussianHMM(n_components=n_states)
        model.startprob = np.array(startProb.values)
        model.transmat = np.array(transProb.values)
        model.emissionprob = np.array(obsProb.values)

        # predict a sequence of hidden states based on visible states
        bob_says = np.array([[0, 2, 1, 1, 2, 0]]).T
        bob = np.array([emissions]).T
        model = model.fit(bob)
        logprob, alice_hears = model.decode(bob, algorithm="viterbi")
        print("Bob says:", ", ".format(bob))
        print("Bob says:", ", ".format(alice_hears))
        print("Bob says:", ", ".format(giusti))

