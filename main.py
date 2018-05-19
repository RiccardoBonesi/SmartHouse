from csv_generator import *

if __name__ == '__main__':

    ordonezA = ['Dataset/OrdonezA', 'Dataset/OrdonezA_Description', 'Dataset/OrdonezA_ADLs', 'Dataset/OrdonezA_Sensors']
    ordonezB = ['Dataset/OrdonezB', 'Dataset/OrdonezB_Description', 'Dataset/OrdonezB_ADLs', 'Dataset/OrdonezB_Sensors']
    dataset = [ordonezA, ordonezB]

    for house in dataset:
        data = elaborate_dataset(house)
