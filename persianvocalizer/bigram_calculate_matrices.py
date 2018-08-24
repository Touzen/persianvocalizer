from collections import defaultdict
import math

observations = defaultdict(lambda: defaultdict(float))
states = defaultdict(lambda: defaultdict(float))
state_set = set()
with open('training.dat', 'r') as training:
    for line in training:
        in_observations, in_states = eval(line)
        for observation, state in zip(in_observations, in_states):
            observations[observation][state] += 1
            state_set.add(state)

        prev_state = '^'
        state_set.add('^')
        for state in in_states:
            states[prev_state][state] += 1
            prev_state = state
        states[prev_state]['$'] += 1
        state_set.add('$')

#SMOOOTH
for s in state_set:
    for s2 in state_set:
        states[s][s2] += 1

for observation in observations.keys():
    for state in state_set:
        observations[observation][state] += 1

# NORMALIZE
for _, prev_state in states.items():
    transitions = sum(count for _, count in prev_state.items())
    for state in prev_state.keys():
        prev_state[state] = math.log(prev_state[state]/transitions)

for _, observation in observations.items():
    n_emissions = sum(count for _, count in observation.items())
    for emission in observation.keys():
        observation[emission] = math.log(observation[emission]/n_emissions)

o_indices = {observation: index for index, observation in enumerate(observations.keys())}
s_indices = {state: index for index, state in enumerate(state_set)}

with open('a_matrix_bigram.dat', 'w') as a_file:
    for prev_state in states.keys():
        for state in states[prev_state].keys():
            logprob = states[prev_state][state]
            a_file.write('%d\t%d\t%.16f\n'%(s_indices[prev_state], s_indices[state], logprob))

with open('b_matrix_bigram.dat', 'w') as b_file:
    for observation in observations.keys():
        for state in observations[observation].keys():
            o_index = o_indices[observation]
            s_index = s_indices[state]
            logprob = observations[observation][state]
            b_file.write('%d\t%d\t%.16f\n'%(o_index, s_index, logprob))

with open('observation_indices.dat', 'w') as o_file:
    for observation, index in o_indices.items():
        o_file.write('%s\t%d\n'%(observation, index))

with open('state_indices.dat', 'w') as s_file:
    for state, index in s_indices.items():
        s_file.write('%s\t%d\n'%(state, index))
