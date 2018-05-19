import numpy

import pandas as pd

def obtain_p_adls():
    dataset = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']

    activities=[]
    dataCount = []
    startProb=[]
    for currentDataset in dataset:
        data = pd.read_csv(currentDataset, sep="\t\t")
        activities.append(data['Activity'].unique())
        dataCount.append(data['Activity'].value_counts())
        s = sum(data['Activity'].value_counts());
        norm = [float(i) / s for i in data['Activity'].value_counts()]
        startProb.append(norm)

    print("")

    # for house in dataset:


    #  tot_rows = len(open(path_file + '.csv').readlines())
    #  list_adls = []
    #  p_adls = []
    # seq_adls = []
    # with open(path_file + '.csv', 'rb') as csvfile:
    #     reader = csv.reader(csvfile, dialect='excel', delimiter='\t')
    #     for row in reader:
    #         adl = copy.deepcopy(row[2])
    #         exist_adl = False
    #         for c, a in enumerate(list_adls):
    #             if (a == adl):
    #                 p_adls[c] += 1
    #                 exist_adl = True
    #                 seq_adls.append(c)
    #         if not exist_adl:
    #             list_adls.append(adl)
    #             p_adls.append(1)
    #             seq_adls.append(len(list_adls) - 1)
    #     normalize_list(p_adls)
    # print '%s: P(ADLs) calculated' % house_name
    # csv_list(list_adls, p_adls, house_name + '_P(ADLs)')
    # return list_adls, p_adls, seq_adls