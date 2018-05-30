from datset_utils import *
from probability_calc import *
from hmm import *

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
        evidences = mergedDataset['Activity'].unique().tolist()
        giusti = test['Activity'].values.flatten()
        for idx, val in enumerate(giusti):
            giusti[idx] = evidences.index(val)

        # OLD HMM
        viterbi_result,b,c = viterbi(emissions,transProb.values,obsProb.values,startProb.values.flatten())

        # CONTO QUANTI STATI HO INDOVINATO
        result = 0
        for ind, val in enumerate(viterbi_result):
            if val == giusti[ind]:
                result = result + 1


        print("DATASET: {}".format(dataset))
        print("Stati effettivi: {}".format(giusti))
        print("Stati predetti: {}".format(viterbi_result))
        print("Stati corretti: {} su {}".format(result, len(test)))

