from datset_utils import *
from probability_calc import *
from hmm import *
from preprocessing import *
from time_slice import *


# NOTA: per debuggare questo file senza usare la GUI
# decommentare il  if __name__ == '__main__': sotto il metodo calculate

# CREO TRAIN E TEST SET PER DATASET A
def create_set_A(mergedDataset, days):
    # test da 2 giorni
    if days == 1:
        trainIndex = range(0, 367)
        testIndex = range(368, len(mergedDataset.index))
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 2:
        trainIndex = range(68, len(mergedDataset.index))
        testIndex = range(0, 67)
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 3:
        trainIndex = range(0, 247)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(319,len(mergedDataset.index)),:])
        testIndex = range(248, 318)
        test = mergedDataset.loc[testIndex, :]
    elif days == 4:
        trainIndex = range(0, 318)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(367, len(mergedDataset.index)), :])
        testIndex = range(319, 366)
        test = mergedDataset.loc[testIndex, :]
    elif days == 5:
        trainIndex = range(0, 105)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(159, len(mergedDataset.index)), :])
        testIndex = range(106, 158)
        test = mergedDataset.loc[testIndex, :]
    # test da 3 giorni
    elif days == 6:
        trainIndex = range(0, 339)
        testIndex = range(340, len(mergedDataset.index))
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 7:
        trainIndex = range(106, len(mergedDataset.index))
        testIndex = range(0, 105)
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 8:
        trainIndex = range(0, 205)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(319,len(mergedDataset.index)),:])
        testIndex = range(206, 318)
        test = mergedDataset.loc[testIndex, :]
    elif days == 9:
        trainIndex = range(0, 278)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(367, len(mergedDataset.index)), :])
        testIndex = range(279, 366)
        test = mergedDataset.loc[testIndex, :]
    elif days == 10:
        trainIndex = range(0, 67)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(159, len(mergedDataset.index)), :])
        testIndex = range(68, 158)
        test = mergedDataset.loc[testIndex, :]



    return train, test


def create_set_B(mergedDataset, days):
    # test da 2 giorni
    if days == 1:
        trainIndex = range(0, 580)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(808, len(mergedDataset.index)), :])
        testIndex = range(581, 807)
        test = mergedDataset.loc[testIndex, :]
    elif days == 2:
        trainIndex = range(0, 1827)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(2079, len(mergedDataset.index)), :])
        testIndex = range(1828, 2078)
        test = mergedDataset.loc[testIndex, :]
    elif days == 3:
        trainIndex = range(0, 15)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(275, len(mergedDataset.index)), :])
        testIndex = range(16, 274)
        test = mergedDataset.loc[testIndex, :]
    elif days == 4:
        trainIndex = range(0, 1706)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1963, len(mergedDataset.index)), :])
        testIndex = range(1707, 1962)
        test = mergedDataset.loc[testIndex, :]
    elif days == 5:
        trainIndex = range(0, 1105)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1302, len(mergedDataset.index)), :])
        testIndex = range(1106, 1301)
        test = mergedDataset.loc[testIndex, :]
    # test da 7 giorni
    elif days == 6:
        trainIndex = range(0, 580)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1425, len(mergedDataset.index)), :])
        testIndex = range(581, 1424)
        test = mergedDataset.loc[testIndex, :]
    elif days == 7:
        trainIndex = range(0, 1206)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1964, len(mergedDataset.index)), :])
        testIndex = range(1207, 1963)
        test = mergedDataset.loc[testIndex, :]
    elif days == 8:
        trainIndex = range(0, 15)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(809, len(mergedDataset.index)), :])
        testIndex = range(16, 808)
        test = mergedDataset.loc[testIndex, :]
    elif days == 9:
        trainIndex = range(0, 1004)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1708, len(mergedDataset.index)), :])
        testIndex = range(1005, 1707)
        test = mergedDataset.loc[testIndex, :]
    elif days == 10:
        trainIndex = range(0, 1105)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(1825, len(mergedDataset.index)), :])
        testIndex = range(1106, 1824)
        test = mergedDataset.loc[testIndex, :]


    return train,test


# predizione sul dataset dt
def calculate(dt, days, method):

    if method==1:
        # NO TIME SLICE
        if dt == 1:
            dataset = 'Dataset/OrdonezA_ADLs.txt'
            sensor = 'Dataset/OrdonezA_Sensors.txt'
        else:
            dataset = 'Dataset/OrdonezB_ADLs.txt'
            sensor = 'Dataset/OrdonezB_Sensors.txt'

        mergedDataset = merge_dataset(dataset, sensor)

        # CREO TRAIN E TEST SET
        if dataset == 'Dataset/OrdonezA_ADLs.txt':
            train, test = create_set_A(mergedDataset, days)
        else:
            train, test = create_set_B(mergedDataset, days)

        startProb = get_start_prob(train)
        transProb = get_trans_prob(train, dt)
        obsProb = get_obs_prob(train, dt)

        # CONVERTO OSSERVAZIONI IN NUMERI
        evidences = mergedDataset['Evidence'].unique().tolist()
        emissions = test['Evidence'].values.flatten()
        for idx, val in enumerate(emissions):
            emissions[idx] = evidences.index(val)

        # CONVERTO GLI STATI IN NUMERI
        states = mergedDataset['Activity'].unique().tolist()
        giusti = test['Activity'].values.flatten()
        for idx, val in enumerate(giusti):
            giusti[idx] = states.index(val)

        # VITERBI
        viterbi_result, b, c = hmm.viterbi(emissions, transProb.values, obsProb.values, startProb.values.flatten())

        # CONTO QUANTI STATI HO INDOVINATO
        result = 0
        for ind, val in enumerate(viterbi_result):
            if val == giusti[ind]:
                result = result + 1

        print("DATASET: {}".format(dataset))
        print("Stati effettivi: {}".format(giusti))
        print("Stati predetti: {}".format(viterbi_result))
        print("Stati corretti: {} su {}".format(result, len(test)))


        accuracy = (result * 100) / len(test)
        print("Accuratezza: {}".format(accuracy))


    else:
        # TIME SLICE
        giusti, viterbi_result, accuracy = slice_prob(dt, days)




    return viterbi_result, giusti, accuracy






if __name__ == '__main__':
    # 1=dataset A, 2=dataset B
    # datset, days, method(1=no Time Slice)
    calculate(1, 2, 2)


