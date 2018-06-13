from preprocessing import *
from hmm import *

import pytz


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
        # DATASET A: TRAIN E TEST SET
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

        elif days == 5:
            trainIndex = range(0, 4063)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(6619, len(df.index)), :])
            testIndex = range(4064, 6618)
            test = df.loc[testIndex, :]

    else :
        # DATASET A: TRAIN E TEST SET
        if days == 1:
            trainIndex = range(0, 6673)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(9036, len(df.index)), :])
            testIndex = range(6674, 9035)
            test = df.loc[testIndex, :]

        elif days == 2:
            trainIndex = range(0, 22329)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(24809, len(df.index)), :])
            testIndex = range(22330, 24808)
            test = df.loc[testIndex, :]

        elif days == 3:
            trainIndex = range(0, 275)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(2672, len(df.index)), :])
            testIndex = range(276, 2671)
            test = df.loc[testIndex, :]

        elif days == 4:
            trainIndex = range(0, 21092)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(23564, len(df.index)), :])
            testIndex = range(21091, 23563)
            test = df.loc[testIndex, :]

        elif days == 5:
            trainIndex = range(0, 13164)
            train = df.loc[trainIndex, :]
            train = train.append(df.loc[range(15765, len(df.index)), :])
            testIndex = range(13165, 15764)
            test = df.loc[testIndex, :]
        # DATASET B: TRAIN E TEST SET


    trainset_s = train['activity']
    trainset_o = train['sensors']
    testset_s = test['activity'].tolist()
    testset_o = test['sensors'].tolist()
    size = test.shape[0]



    # Calcolo delle distribuzioni della HMM
    P = prior(trainset_s)
    T = transition_matrix(trainset_s)
    O = obs_matrix(trainset_s, trainset_o)

    viterbi_result, p, x = hmm.viterbi(testset_o, T, O, P)
    c = 0
    for i, j in zip(viterbi_result, testset_s):
        if i == j:
            c += 1

    accuracy = c/len(viterbi_result) * 100

    return testset_s, viterbi_result, accuracy




# if __name__ == '__main__':
#     slice_prob(1,2)