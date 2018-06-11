import pandas as pd
import numpy as np
from ast import literal_eval
from pomegranate import HiddenMarkovModel, DiscreteDistribution, State


pd.set_option('display.expand_frame_repr', False)
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)

def probability_distribution(seq1, seq2):
    n = 1 + max(seq1); m = 1 + max(seq2)
    M = np.zeros((n, m))

    # Conta delle occorrenze
    for s1, s2 in zip(seq1, seq2):
        M[s1][s2] += 1

    # Calcolo delle distribuzioni di probabilità
    row_sums = M.sum(axis=1)
    M = M / row_sums[:, np.newaxis]

    return M


# Calcola la distribuzione di probabilità degli stati
def prior(transitions):
    g = transitions.groupby(transitions)
    result = g.count()/g.count().sum()
    return result.as_matrix()


# Calcola la matrice di transizione data la sequenza di stati ad ogni tempo t
def transition_matrix(sequence):
    return probability_distribution(sequence, sequence[1:])


# Calcola la distribuzione di probabilità delle osservazioni per ogni stato
def obs_matrix(seq, obs):
    return probability_distribution(seq, obs)


def main():
    for f in ['A', 'B']:
        df = pd.read_csv(f'dataset_csv/Ordonez{f}.csv',
            converters={'sensors': str})

        # Discretizza le osservazioni dei sensori
        df[['sensors']] = df[['sensors']].apply(lambda x: x.astype('category'))
        mapping = dict(enumerate(df['sensors'].cat.categories))
        df[['sensors']] = df[['sensors']].apply(lambda x: x.cat.codes)

        # TODO: Suddividere in train e test set
        size = int(df.shape[0]*0.8)
        trainset_s = df['activity'][:size]; testset_s = df['activity'].tolist()[size:]
        trainset_o = df['sensors'][:size]; testset_o = df['sensors'].tolist()[size:]

        P = prior(trainset_s)
        T = transition_matrix(trainset_s)
        O = obs_matrix(trainset_s, trainset_o)

        x, T1, T2 = viterbi(testset_o, T, O, P)
        c = 0
        for i, j in zip(x, testset_s):
            if i == j:
                c += 1
        print(c/len(x))

    #     model = HiddenMarkovModel(name=f"model{f}")
    #     # Inizializzazione gli stati
    #     states = []
    #     for i in range(O.shape[0]):
    #         d = dict(enumerate(O[i,:]))
    #         states.append(State(DiscreteDistribution(d), name=f'{i}'))
    #     model.add_states(*states)

    #     # Definizione delle probabilità iniziali
    #     for i, p in enumerate(P):
    #         model.add_transition(model.start, states[i], p)

    #     # Definizione delle transizioni tra stati
    #     for i, s1 in enumerate(states):
    #         for j, s2 in enumerate(states):
    #             model.add_transition(s1, s2, T[i, j])

    # #           (
    # #            )
    # #       __..---..__
    # #   ,-='  /  |  \  `=-.
    # #  :--..___________..--;
    # #   \.,_____________,./
    #     model.bake()
    #     # import pdb; pdb.set_trace()
    #     res = model.viterbi(testset_o)
    #     seq = [i for i, s in res[1]]
    #     seq = seq[1:]
    #     c = 0
    #     for i, j in zip(seq, testset_s):
    #         if i == j:
    #             c += 1

    #     print(c/len(seq))

    return P, T, O


def viterbi(y, A, B, Pi=None):
    """
    Return the MAP estimate of state trajectory of Hidden Markov Model.

    Parameters
    ----------
    y : array (T,)
        Observation state sequence. int dtype.
    A : array (K, K)
        State transition matrix. See HiddenMarkovModel.state_transition  for
        details.
    B : array (K, M)
        Emission matrix. See HiddenMarkovModel.emission for details.
    Pi: optional, (K,)
        Initial state probabilities: Pi[i] is the probability x[0] == i. If
        None, uniform initial distribution is assumed (Pi[:] == 1/K).

    Returns
    -------
    x : array (T,)
        Maximum a posteriori probability estimate of hidden state trajectory,
        conditioned on observation sequence y under the model parameters A, B,
        Pi.
    T1: array (K, T)
        the probability of the most likely path so far
    T2: array (K, T)
        the x_j-1 of the most likely path so far
    """
    # Cardinality of the state space
    K = A.shape[0]
    # Initialize the priors with default (uniform dist) if not given by caller
    Pi = Pi if Pi is not None else np.full(K, 1 / K)
    T = len(y)
    T1 = np.empty((K, T), 'd')
    T2 = np.empty((K, T), 'B')

    # Initilaize the tracking tables from first observation
    T1[:, 0] = Pi * B[:, y[0]]
    T2[:, 0] = 0

    # Iterate throught the observations updating the tracking tables
    for i in range(1, T):
        T1[:, i] = np.max(T1[:, i - 1] * A.T * B[np.newaxis, :, y[i]].T, 1)
        T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)

    # Build the output, optimal model trajectory
    x = np.empty(T, 'B')
    x[-1] = np.argmax(T1[:, T - 1])
    for i in reversed(range(1, T)):
        x[i - 1] = T2[x[i], i]

    return x, T1, T2



if __name__ == '__main__':
    main()
