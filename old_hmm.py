from bayespy.nodes import Categorical, Mixture
from bayespy.inference import VB
from bayespy.nodes import CategoricalMarkovChain


def build_hmm(start_prob,trans_prob, obs_prob, merged_dataset):
    asd = start_prob.values[0]
    asd2 = trans_prob.values
    asd3 = obs_prob.values
    Z = CategoricalMarkovChain(start_prob.values[0], trans_prob.values, states=len(merged_dataset))
    Y = Mixture(Z, Categorical, obs_prob.values)
    states = Z.random()
    observation = Mixture(states, Categorical, obs_prob.values).random()
    evidences = merged_dataset['Evidence'].unique().tolist()

    num_evidence = []

    for i in range(len(merged_dataset)):
        ev = merged_dataset['Evidence'][i]
        index = evidences.index(ev)
        num_evidence.append(index)


    Y.observe(num_evidence)
    Q = VB(Y, Z)
    asd5 = Q.update()
    print("ciao")





# <class 'list'>: ['BedPressureBedroom', 'CabinetMagneticBathroom', 'BasinPIRBathroom', 'ToiletFlushBathroom', 'ShowerPIRBathroom', 'FridgeMagneticKitchen', 'CupboardMagneticKitchen', 'ToasterElectricKitchen', 'CooktopPIRKitchen', 'MicrowaveElectricKitchen', 'SeatPressureLiving', 'MaindoorMagneticEntrance']