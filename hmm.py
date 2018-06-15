import numpy as np
class hmm(object):

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
        B = np.log10(B)
        A = np.log10(A)
        Pi = np.log10(Pi)
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
            T1[:, i] = np.max(T1[:, i - 1] + A.T + B[np.newaxis, :, y[i]].T, 1)
            T2[:, i] = np.argmax(T1[:, i - 1] + A.T, 1)

        # Build the output, optimal model trajectory
        x = np.empty(T, 'B')
        x[-1] = np.argmax(T1[:, T - 1])
        for i in reversed(range(1, T)):
            x[i - 1] = T2[x[i], i]

        return x, T1, T2

    # def test_forward(self):
    #     # test usando l'assignment "hmm filtering" su elearning
    #     p = np.array([0.98, 0.02])
    #     T = np.array([[0.4, 0.6], [0.1, 0.9]])
    #     O = np.array([[0.8, 0.2], [0.1, 0.9]])
    #     oss = np.array([0, 1, 1])
    #     forward_prob = self.forward(oss, T, O, p)
    #     print(forward_prob)


    # def forward(self,obs, A, B, pi):
    #     # obs = observation list, A = Transition probs, B = Emission Probs, pi = initial distribution
    #     fwd = [{}]
    #     states = A.shape[0]
    #     # Initialize base cases (t == 0)
    #     for y in range(states):
    #         fwd[0][y] = pi[y] * B[y][obs[0]]
    #     # Run Forward algorithm for t > 0
    #     for t in range(1, len(obs)):
    #         fwd.append({})
    #         for y in range(states):
    #             fwd[t][y] = sum((fwd[t - 1][y0] * A[y0][y] * B[y][obs[t]]) for y0 in range(states))
    #     prob = sum((fwd[len(obs) - 1][s]) for s in range(states))
    #     return prob
    #
    # def viterbi_old(self,obs, A, B, pi):
    #     vit = [{}]
    #     path = {}
    #     # Initialize base cases (t == 0)
    #     states = A.shape[0]
    #     for y in range(states):
    #         vit[0][y] = pi[y] * B[y][obs[0]]
    #         path[y] = [y]
    #
    #     # Run Viterbi for t > 0
    #     for t in range(1, len(obs)):
    #         vit.append({})
    #         newpath = {}
    #         for y in range(states):
    #             (prob, state) = max((vit[t - 1][y0] * A[y0][y] * B[y][obs[t]], y0) for y0 in range(states))
    #             vit[t][y] = prob
    #             newpath[y] = path[state] + [y]
    #             # Don't need to remember the old paths
    #         path = newpath
    #     n = 0  # if only one element is observed max is sought in the initialization values
    #     if len(obs) != 1:
    #         n = t
    #     (prob, state) = max((vit[n][y], y) for y in range(states))
    #     return (prob, path[state])
    #
    #
    # def forward_backward(self, obs, A, B, pi):  # returns model given the initial model and observations
    #     states = A.shape[0]
    #     gamma = [{} for t in
    #              range(len(obs))]  # this is needed to keep track of finding a state i at a time t for all i and all t
    #     zi = [{} for t in range(len(
    #         obs) - 1)]  # this is needed to keep track of finding a state i at a time t and j at a time (t+1) for all i and all j and all t
    #     # get alpha and beta tables computes
    #     p_obs = self.forward(obs, A, B, pi)
    #     self.backward(obs, A, B, pi)
    #     # compute gamma values
    #     for t in range(len(obs)):
    #         for y in range(states):
    #             gamma[t][y] = (self.fwd[t][y] * self.bwk[t][y]) / p_obs
    #             if t == 0:
    #                 pi[y] = gamma[t][y]
    #             # compute zi values up to T - 1
    #             if t == len(obs) - 1:
    #                 continue
    #             zi[t][y] = {}
    #             for y1 in range(states):
    #                 zi[t][y][y1] = self.fwd[t][y] * A[y][y1] * B[y1][obs[t + 1]] * self.bwk[t + 1][y1] / p_obs
    #     # now that we have gamma and zi let us re-estimate
    #     for y in range(states):
    #         for y1 in range(states):
    #             # we will now compute new a_ij
    #             val = sum([zi[t][y][y1] for t in range(len(obs) - 1)])  #
    #             val /= sum([gamma[t][y] for t in range(len(obs) - 1)])
    #             A[y][y1] = val
    #     # re estimate gamma
    #     for y in range(states):
    #         for k in self.symbols:  # for all symbols vk
    #             val = 0.0
    #             for t in range(len(obs)):
    #                 if obs[t] == k:
    #                     val += gamma[t][y]
    #             val /= sum([gamma[t][y] for t in range(len(obs))])
    #             B[y][k] = val
    #     return