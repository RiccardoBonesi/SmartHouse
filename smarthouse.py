import pandas as pd
import numpy as np
from datetime import *
from preprocessing import *
from hmm import *

import pytz

pd.set_option('display.expand_frame_repr', False)
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)


def probability_distribution(seq1, seq2):
    n = 1 + max(seq1);
    m = 1 + max(seq2)
    M = np.zeros((n, m))

    # Conta delle occorrenze
    for s1, s2 in zip(seq1, seq2):
        M[s1][s2] += 1

    # Pone a 'epsilon' le probabilità che sono zero
    M[M == 0] = 10e-2

    # Calcolo delle distribuzioni di probabilità
    row_sums = M.sum(axis=1)
    M = M / row_sums[:, np.newaxis]

    return M


# Calcola la distribuzione di probabilità degli stati
def prior(transitions):
    g = transitions.groupby(transitions)
    result = g.count() / g.count().sum()
    return result.as_matrix()


# Calcola la matrice di transizione data la sequenza di stati ad ogni tempo t
def transition_matrix(sequence):
    return probability_distribution(sequence, sequence[1:])


# Calcola la distribuzione di probabilità delle osservazioni per ogni stato
def obs_matrix(seq, obs):
    return probability_distribution(seq, obs)


def date_to_timestamp(m):
    return int(datetime.strptime(m.strip(), "%Y-%m-%d %H:%M:%S").timestamp())


def print_numpy_matrix(m):
    import sys
    np.savetxt(sys.stdout, m, '%6.4f')


# def viterbi(initial, transition, emission, events):
#     """Find the likeliest path in a hidden Markov Model resulting in the
#     given events.
#     Arguments:
#     initial: arraylike(n) --- probability of starting in each state
#     transition: arraylike(n, n) -- probability of transition between states
#     emission: arraylike(n, e) -- probability of emitting each event in
#         each state
#     events -- iterable of events
#     Returns:
#     path: list(int) -- list of states in the most probable path
#     p: float -- log-likelihood of that path
#     """
#     # Use log-likelihoods to avoid floating-point underflow. Note that
#     # we want -inf for the log of zero, so suppress warnings here.
#     with np.errstate(divide='ignore'):
#         initial = np.log10(initial)
#         transition = np.log10(transition)
#         emission = np.log10(emission)
#
#
#     # List of arrays giving most likely previous state for each state.
#     prev = []
#
#     events = iter(events)
#     logprob = initial + emission[:, next(events)]
#     for event in events:
#         # p[i, j] is log-likelihood of being in state j, having come from i.
#         p = logprob[:, np.newaxis] + transition + emission[:, event]
#         prev.append(np.argmax(p, axis=0))
#         logprob = np.max(p, axis=0)
#
#     # Most likely final state.
#     best_state = np.argmax(logprob)
#
#     # Reconstruct path by following links and then reversing.
#     state = best_state
#     path = [state]
#     for p in reversed(prev):
#         state = p[state]
#         path.append(state)
#     return path[::-1], logprob[best_state]


# Genera una sequenza di stati e di osservazioni campionando utilizzando le
# distribuzioni di probabilità che definiscono la HMM.
# def random_sample(P, T, O, n):
#     assert(n > 0)
#     states = []; obs = []
#     states.append(np.random.choice(range(len(P)), p=P))
#     obs.append(np.random.choice(range(O.shape[1]), p=O[states[0]]))
#
#     i = 0
#     while i < n:
#         new_state = np.random.choice(range(len(P)), p=T[states[-1]])
#         new_obs = np.random.choice(range(O.shape[1]), p=O[states[-1]])
#         states.append(new_state); obs.append(new_obs)
#         i += 1
#
#     return states, obs


# CALCOLA LE MATRICI DI PROBABILITA' PER I TIME SLICE
def slice_prob(dt, days, train_rate=0.75, to_date=None, n_samples=0, length=None):
    res = []

    if dt == 1:
        try:
            # prende il dataset mergiato dal csv
            df = pd.read_csv('dataset_csv/OrdonezA.csv')
        except:
            # se non trova il csv esegue il preprocessing
            df = generate_dataset()[0]
    else:
        try:
            # prende il dataset mergiato dal csv
            df = pd.read_csv('dataset_csv/OrdonezB.csv')
        except:
            # se non trova il csv esegue il preprocessing
            df = generate_dataset()[1]


    # Discretizza le osservazioni dei sensori
    df[['sensors']] = df[['sensors']].apply(lambda x: x.astype('category'))
    mapping = dict(enumerate(df['sensors'].cat.categories))
    df[['sensors']] = df[['sensors']].apply(lambda x: x.cat.codes)

    df['date'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x, tz=pytz.UTC))

    if dt == 1:
        # if days == 1:
        #     # 16402 to lenght
        #     trainIndex = range(0, 16401)
        #     testIndex = range(16402, len(mergedDataset.index))
        #     train = mergedDataset.loc[trainIndex, :]
        #     test = mergedDataset.loc[testIndex, :]
        # elif days == 2:
        #      trainIndex = range(2371, len(df.index))
        #      testIndex = range(0, 2370)
        #      train = df.loc[trainIndex, :]
        #      test = df.loc[testIndex, :]
        # elif days == 3:
        #     trainIndex = range(0, 10930)
        #     train = df.loc[trainIndex, :]
        #     train = train.append(df.loc[range(13544, len(df.index)), :])
        #     testIndex = range(10931, 13543)
        #     test = df.loc[testIndex, :]
        # elif days == 4:
        #     trainIndex = range(0, 318)
        #     train = mergedDataset.loc[trainIndex, :]
        #     train = train.append(mergedDataset.loc[range(367, len(mergedDataset.index)), :])
        #     testIndex = range(319, 366)
        #     test = mergedDataset.loc[testIndex, :]
        # elif days == 5:
        #     trainIndex = range(0, 105)
        #     train = mergedDataset.loc[trainIndex, :]
        #     train = train.append(mergedDataset.loc[range(159, len(mergedDataset.index)), :])
        #     testIndex = range(106, 158)
        #     test = mergedDataset.loc

        if days == 1:
            trainIndex = range(0, 16401)
            testIndex = range(16402, len(df.index))
            train = df.loc[trainIndex, :]
            test = df.loc[testIndex, :]

        elif days == 2:
            trainIndex = range(2371, len(df.index))
            testIndex = range(0, 2370)
            train = df.loc[trainIndex, :]
            test = df.loc[testIndex, :]

        elif days == 3:
            trainIndex = range(0, 10930)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(13544, len(df.index)), :])
            testIndex = range(10931, 13543)
            test = df.loc[testIndex, :]

        elif days == 4:
            trainIndex = range(0, 13676)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(16402, len(df.index)), :])
            testIndex = range(13677, 16401)
            test = df.loc[testIndex, :]


    trainset_s = train['activity']
    trainset_o = train['sensors']
    testset_s = test['activity'].tolist()
    testset_o = test['sensors'].tolist()
    size = test.shape[0]



    # Calcolo delle distribuzioni della HMM
    P = prior(trainset_s)
    T = transition_matrix(trainset_s)
    O = obs_matrix(trainset_s, trainset_o)

    # return P, T, O

    # Esegue l'algoritmo di Viterbi sul testset e calcola
    # calcola la percentuale di stati predetti correttamente
    # seq, p = viterbi(P, T, O, testset_o)
    # c = 0
    # for i, j in zip(seq, testset_s):
    #     if i == j:
    #         c += 1
    # print(f"Dataset {f}, trainset: {size}: {c/len(seq):.3f}")
    # print(seq)
    # res.append(c/len(seq))
    # print(res)

    # y, A, B, Pi = None

    viterbi_result, p, x = hmm.viterbi(testset_o, T, O, P)
    c = 0
    for i, j in zip(viterbi_result, testset_s):
        if i == j:
            c += 1



    accuracy = c/len(viterbi_result) * 100
    # print(accuracy)

    # list_pred, pred, list_truth, n_states, accuracy
    # list_truth, list_pred, accuracy

    return testset_s, viterbi_result, accuracy


# return res

if __name__ == '__main__':
    slice_prob(1,2)