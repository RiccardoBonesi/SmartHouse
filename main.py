from csv_generator import *
from probability_calc import *
from hidden_markov_model import *
from old_hmm import *

if __name__ == '__main__':

    datasetList = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']
    sensorList = ['Dataset/OrdonezA_Sensors.txt', 'Dataset/OrdonezB_Sensors.txt']
    for dataset in datasetList:
        mergedDataset = merge_dataset(dataset, sensorList[datasetList.index(dataset)])

        if (dataset == 'Dataset/OrdonezA_ADLs.txt'):
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

        evidences = mergedDataset['Evidence'].unique().tolist()
        emissions = test['Evidence'].values.flatten()
        for idx, val in enumerate(emissions):
            emissions[idx] = evidences.index(val)

        hmm = HMM(transProb.values, obsProb.values)
        # vit = viterbi(hmm, startProb.values.flatten(), emissions.flatten())

        evidences = mergedDataset['Activity'].unique().tolist()
        arrr2 = test['Activity'].values.flatten()
        for idx, val in enumerate(arrr2):
            arrr2[idx] = evidences.index(val)





        # OLD HMM
        a,b,c = viterbi_2(emissions,transProb.values,obsProb.values,startProb.values.flatten())

        result = 0
        for ind, val in enumerate(a):
            if (val == arrr2[ind]):
                result = result + 1


        print("dio")

        # NEW VITERBI
        # evidences = mergedDataset['Evidence'].unique().tolist()
        # arrr = test['Evidence'].values.flatten()
        # for idx, val in enumerate(arrr):
        #
        #     arrr[idx] = int(evidences.index(val))
        #     if isinstance(arrr[idx], str):
        #         print("stringa")
        #     if isinstance(arrr[idx], int):
        #         print("int")
        #
        #
        #
        #
        # asdone = transProb.values
        # asdtwo = obsProb.values
        # hmm = HMM(transProb.values, obsProb.values)
        # vit = viterbi(hmm, startProb.values, arrr)
        #
        # evidences = mergedDataset['Activity'].unique().tolist()
        # arrr2 = test['Activity'].values.flatten()
        # for idx, val in enumerate(arrr2):
        #     arrr2[idx] = evidences.index(val)
        #
        #
        # result = 0
        # for ind, val in enumerate(vit):
        #     if (val == arrr2[ind]):
        #         result = result + 1
        # result
        # print(viterbi(hmm, startProb.values, arrr))
        #
        # prova = viterbi_alg(transProb.values,obsProb.values, arrr)
        #
        # print("calcolate tutte le probabilità per il dataset {}".format(datasetList[datasetList.index(dataset)]))















    # ordonezA = ['Dataset/OrdonezA', 'Dataset/OrdonezA_Description', 'Dataset/OrdonezA_ADLs', 'Dataset/OrdonezA_Sensors']
    # ordonezB = ['Dataset/OrdonezB', 'Dataset/OrdonezB_Description', 'Dataset/OrdonezB_ADLs', 'Dataset/OrdonezB_Sensors']
    # dataset = [ordonezA, ordonezB]

    # for house in dataset:
        # data = elaborate_dataset(house)

    # house_name = house[0]
    # path_adls = house[2]
    # path_sens = house[3]



    # PROBABILITA' TOTALI: numero di occorrenze delle attività





    # temp = obtain_p_adls(path_adls, house_name)
    # list_adls = temp[0]
    # p_adls = temp[1]
    # seq_adls = temp[2]
    # t_adls = obtain_t_adls(path_adls, list_adls, house_name)
    #
    # temp = obtain_list_sens(path_sens, house_name)
    # list_sens = temp[0]
    # seq_sens = temp[1]
    # o_sens_adls = obtain_o_sens_adls(path_adls, list_adls, path_sens, list_sens, house_name)
    #
    # print
    # print
    # 'list sensors: index - name'
    # for x in range(len(list_sens)):
    #     print
    #     '\t%s\t%s' % (x, list_sens[x])
    #
    # print
    # print
    # 'list activity: index - name'
    # for x in range(len(list_adls)):
    #     print
    #     '\t%s\t%s' % (x, list_adls[x])
    #
    # return house_name, path_adls, list_adls, p_adls, seq_adls, t_adls, path_sens, list_sens, seq_sens, o_sens_adls
