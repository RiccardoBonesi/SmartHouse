from csv_generator import *
from probability_calc import *
from hidden_markov_model import *
from old_hmm import *

if __name__ == '__main__':

    datasetList = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']
    sensorList = ['Dataset/OrdonezA_Sensors.txt', 'Dataset/OrdonezB_Sensors.txt']
    for dataset in datasetList:
        mergedDataset = merge_dataset(dataset, sensorList[datasetList.index(dataset)])
        startProb = get_start_prob(mergedDataset)
        transProb = get_trans_prob(mergedDataset)
        obsProb = get_obs_prob(mergedDataset) # passare mergedDataset

        # OLD HMM
        build_hmm(startProb,transProb,obsProb,mergedDataset)

        # NEW VITERBI
        wiki_transition_probs = np.array([[0.7, 0.4], [0.3, 0.6]])  # 0=Healthy, 1=Fever
        wiki_emissions = [2, 1, 0]
        wiki_emission_probs = np.array([[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]])  # 0=Dizzy, 1=Cold, 2=Normal
        wiki_initial_dist = np.array([[0.6, 0.4]])
        wiki_hmm = HMM(wiki_transition_probs, wiki_emission_probs)

        print(viterbi(wiki_hmm, wiki_initial_dist, wiki_emissions))



        print("calcolate tutte le probabilità per il dataset {}".format(datasetList[datasetList.index(dataset)]))
















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
