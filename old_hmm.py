import numpy as np


class HMM:
    #constructor
    #transition_probs[i, j] is the probability of transitioning to state i from state j
    #emission_probs[i, j] is the probability of emitting emission j while in state i
    def __init__(self, transition_probs, emission_probs):
        self._transition_probs = transition_probs
        self._emission_probs = emission_probs

    #accessors
    def emission_dist(self, emission):
        return self._emission_probs[:, emission]

    @property
    def num_states(self):
        return self._transition_probs.shape[0]

    @property
    def transition_probs(self):
        return self._transition_probs


#the Viterbi algorithm
def viterbi_old(hmm, initial_dist, emissions):
    asd = emissions[0]
    asd2= initial_dist
    asd3 = hmm.emission_dist(emissions[0])
    probs = hmm.emission_dist(emissions[0]) * initial_dist
    stack = []

    for emission in emissions[1:]:
        asd4 = np.row_stack(probs)
        asd5 = hmm.transition_probs
        trans_probs = hmm.transition_probs * np.row_stack(probs)
        max_col_ixs = np.argmax(trans_probs, axis=0)
        probs = hmm.emission_dist(emission) * trans_probs[max_col_ixs, np.arange(hmm.num_states)]

        stack.append(max_col_ixs)

    state_seq = [np.argmax(probs)]

    while stack:
        max_col_ixs = stack.pop()
        state_seq.append(max_col_ixs[state_seq[-1]])

    state_seq.reverse()

    return state_seq

def viterbi_alg(A_mat, O_mat, observations):
    # get number of states
    num_obs = observations.size
    num_states = A_mat.shape[0]
    # initialize path costs going into each state, start with 0
    log_probs = np.zeros(num_states)
    # initialize arrays to store best paths, 1 row for each ending state
    paths = np.zeros( (num_states, num_obs+1 ))
    paths[:, 0] = np.arange(num_states)
    # start looping
    for obs_ind, obs_val in enumerate(observations):
        # for each obs, need to check for best path into each state
        for state_ind in range(num_states):
            # given observation, check prob of each path
            temp_probs = log_probs + \
                         np.log(O_mat[state_ind, obs_val]) + \
                         np.log(A_mat[:, state_ind])
            # check for largest score
            best_temp_ind = np.argmax(temp_probs)
            # save the path with a higher prob and score
            paths[state_ind,:] = paths[best_temp_ind,:]
            paths[state_ind,(obs_ind+1)] = state_ind
            log_probs[state_ind] = temp_probs[best_temp_ind]
    # we now have a best stuff going into each path, find the best score
    best_path_ind = np.argmax(log_probs)
    # done, get out.
    return (best_path_ind, paths, log_probs)

