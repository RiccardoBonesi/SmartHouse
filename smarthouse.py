import pandas as pd
import numpy as np
from datetime import datetime


pd.set_option('display.expand_frame_repr', False)
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

def probability_distribution(seq1, seq2):
    n = 1 + max(seq1); m = 1 + max(seq2)
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
    result = g.count()/g.count().sum()
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


def viterbi(initial, transition, emission, events):
    """Find the likeliest path in a hidden Markov Model resulting in the
    given events.
    Arguments:
    initial: arraylike(n) --- probability of starting in each state
    transition: arraylike(n, n) -- probability of transition between states
    emission: arraylike(n, e) -- probability of emitting each event in
        each state
    events -- iterable of events
    Returns:
    path: list(int) -- list of states in the most probable path
    p: float -- log-likelihood of that path
    """
    # Use log-likelihoods to avoid floating-point underflow. Note that
    # we want -inf for the log of zero, so suppress warnings here.
    with np.errstate(divide='ignore'):
        initial = np.log10(initial)
        transition = np.log10(transition)
        emission = np.log10(emission)


    # List of arrays giving most likely previous state for each state.
    prev = []

    events = iter(events)
    logprob = initial + emission[:, next(events)]
    for event in events:
        # p[i, j] is log-likelihood of being in state j, having come from i.
        p = logprob[:, np.newaxis] + transition + emission[:, event]
        prev.append(np.argmax(p, axis=0))
        logprob = np.max(p, axis=0)

    # Most likely final state.
    best_state = np.argmax(logprob)

    # Reconstruct path by following links and then reversing.
    state = best_state
    path = [state]
    for p in reversed(prev):
        state = p[state]
        path.append(state)
    return path[::-1], logprob[best_state]


# Genera una sequenza di stati e di osservazioni campionando utilizzando le
# distribuzioni di probabilità che definiscono la HMM.
def random_sample(P, T, O, n):
    assert(n > 0)
    states = []; obs = []
    states.append(np.random.choice(range(len(P)), p=P))
    obs.append(np.random.choice(range(O.shape[1]), p=O[states[0]]))

    i = 0
    while i < n:
        new_state = np.random.choice(range(len(P)), p=T[states[-1]])
        new_obs = np.random.choice(range(O.shape[1]), p=O[states[-1]])
        states.append(new_state); obs.append(new_obs)
        i += 1

    return states, obs


def main(train_rate=0.75, to_date=None, n_samples=0, length=None):
    res = []
    for f in ['A', 'B']:
        if length:
            df = pd.read_csv(f'dataset_csv/sliced/Ordonez{f}_{length}.csv',
                converters={'sensors': str})
        else:
            df = pd.read_csv(f'dataset_csv/Ordonez{f}.csv',
            converters={'sensors': str})


        # Discretizza le osservazioni dei sensori
        df[['sensors']] = df[['sensors']].apply(lambda x: x.astype('category'))
        mapping = dict(enumerate(df['sensors'].cat.categories))
        df[['sensors']] = df[['sensors']].apply(lambda x: x.cat.codes)

        # Divisione in testset e trainset
        if to_date:
            slice_at = to_date[f]
            trainset = df[df['timestamp'] < slice_at]
            testset = df[df['timestamp'] >= slice_at]
            trainset_s = trainset['activity']
            trainset_o = trainset['sensors']
            testset_s = testset['activity'].tolist()
            testset_o = testset['sensors'].tolist()
            size = trainset.shape[0]
        elif n_samples > 0:
            trainset_s = df['activity']
            trainset_o = df['sensors']
            size = trainset_s.shape[0]
        else:
            size = int(df.shape[0] * train_rate)
            trainset_s = df['activity'][:size]
            trainset_o = df['sensors'][:size]
            testset_s = df['activity'].tolist()[size:]
            testset_o = df['sensors'].tolist()[size:]
            print(f"Trainset: {trainset_s.shape[0]/df.shape[0]:.3f}")

        # Calcolo delle distribuzioni della HMM
        P = prior(trainset_s)
        T = transition_matrix(trainset_s)
        O = obs_matrix(trainset_s, trainset_o)

        if n_samples > 0:
            testset_s, testset_o = random_sample(P, T, O, n_samples)
            # print(testset_s)

        # Esegue l'algoritmo di Viterbi sul testset e calcola
        # calcola la percentuale di stati predetti correttamente
        seq, p = viterbi(P, T, O, testset_o)
        c = 0
        for i, j in zip(seq, testset_s):
            if i == j:
                c += 1
        print(f"Dataset {f}, trainset: {size}: {c/len(seq):.3f}")
        # print(seq)
        res.append(c/len(seq))

    return res


if __name__ == '__main__':
    main(n_samples=10000, length=600)