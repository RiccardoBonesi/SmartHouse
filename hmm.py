import numpy as np


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


def test_forward():
    # test usando l'assignment "hmm filtering" su elearning
    p = np.array([0.98, 0.02])
    T = np.array([[0.4, 0.6], [0.1, 0.9]])
    O = np.array([[0.8, 0.2], [0.1,0.9]])
    oss = np.array([0,1,1])
    forward_prob = forward(oss,T,O,p)
    print(forward_prob)



def forward(obs, A, B, pi):
    # obs = observation list, A = Transition probs, B = Emission Probs, pi = initial distribution
    fwd = [{}]
    states = A.shape[0]
    # Initialize base cases (t == 0)
    for y in range(states):
        fwd[0][y] = pi[y] * B[y][obs[0]]
    # Run Forward algorithm for t > 0
    for t in range(1, len(obs)):
        fwd.append({})
        for y in range(states):
            fwd[t][y] = sum((fwd[t - 1][y0] * A[y0][y] * B[y][obs[t]]) for y0 in range(states))
    prob = sum((fwd[len(obs) - 1][s]) for s in range(states))
    return prob


