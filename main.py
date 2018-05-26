from csv_generator import *
from probability_calc import *

if __name__ == '__main__':

    datasetList = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']
    sensorList = ['Dataset/OrdonezA_Sensors.txt', 'Dataset/OrdonezB_Sensors.txt']
    for dataset in datasetList:
        mergedDataset = merge_dataset(dataset, sensorList[datasetList.index(dataset)])
        startProb = get_start_prob(dataset)
        transProb = get_trans_prob(dataset)
        obsProb = get_obs_prob(sensorList[datasetList.index(dataset)]) # passare mergedDataset

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
