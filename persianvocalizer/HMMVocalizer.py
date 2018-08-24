import numpy as np
import codecs
import os
import random

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HMMVocalizer(object):
    """
    This class implements Viterbi decoding using bigram probabilities in order
    to find hidden vowels.
    """
    def init_a(self, filename):
        """
        Reads the bigram probabilities (the 'A' matrix) from a file.
        """
        print('Initializing A matrix..')
        with codecs.open(os.path.join(BASE_DIR, filename), 'r', 'utf-8') as f:
            for line in f:
                i, j, d = [func(x) for func, x in zip([int, int, float], line.strip().split('\t'))]
                self.a[i][j] = d

    def init_b(self):
        """
        Initializes the observation probabilities (the 'B' matrix).
        """
        print('Initializing B matrix...')
        with open(os.path.join(BASE_DIR, 'b_matrix_bigram.dat'), 'r') as b_file:
            for line in b_file:
                observation, state, logprob = [func(x) for func, x in zip([int, int, float], line.strip().split('\t'))]
                self.b[observation][state] = logprob if logprob != 0 else -float('inf')

    def init_metadata(self):
        print('Initializing metadata...')
        self.observation_to_index = {}
        self.index_to_observation = {}
        with open(os.path.join(BASE_DIR, 'observation_indices.dat'), 'r') as f:
            for line in f:
                observation, index = [func(x) for func, x in zip([str, int], line.split('\t'))]
                self.observation_to_index[observation] = index
                self.index_to_observation[index] = observation
        self.N_OBSERVATIONS = len(self.observation_to_index)
            
        self.state_to_index = {}
        self.index_to_state = {}
        with open(os.path.join(BASE_DIR, 'state_indices.dat'), 'r') as f:
            for line in f:
                state, index = [func(x) for func, x in zip([str, int], line.split('\t'))]
                self.state_to_index[state] = index
                self.index_to_state[index] = state
        self.N_STATES = len(self.state_to_index)


    def viterbi(self, string):
        """
        Performs the Viterbi decoding and returns the most likely
        string.
        """
        index = []
        for x in string:
            if x not in self.observation_to_index:
                # This means that we have encountered unknown data.
                print("[DEBUG]\tPicking random observation for unknown data: " + x)
                index.append(random.randint(0, self.N_OBSERVATIONS))
            else:
                index.append(self.observation_to_index[x])

        # The Viterbi matrices
        self.v = np.zeros((len(string), self.N_STATES))
        self.v[:,:] = -float("inf")
        self.backptr = np.zeros((len(string) + 1, self.N_STATES), dtype='int')

        # Initialization
        self.backptr[0,:] = self.N_STATES
        self.v[0,:] = self.a[self.state_to_index['^'],:] + self.b[index[0],:]

        # Induction step
        N = self.N_STATES
        T = len(string)
        for t in range(1, T):
            for s in range(N):
                for s_ in range(N):
                    x = self.v[t-1][s_] + self.a[s_][s] + self.b[index[t]][s] 
                    if self.v[t][s] < x:
                        self.v[t][s] = x
                        self.backptr[t][s] = s_

        max_x = -float('inf')
        for s_ in range(N):
                x = self.v[T-1][s_] + self.a[s_][self.state_to_index['$']]
                if x > max_x:
                    max_x = x
                    self.backptr[T][self.state_to_index['$']] = s_

        # Finally return the result
        result = [self.backptr[T][self.state_to_index['$']]]
        for t in range(T-1, -1, -1):
            result.append(self.backptr[t][result[-1]])
        result.reverse()

        return list(map(lambda x: self.index_to_state[x], result[1:]))

    def __init__(self, filename='a_matrix_bigram.dat'):
        """
        Constructor: Initializes the A and B matrices.
        """

        self.init_metadata()

        # The trellis used for Viterbi decoding. The first index is the time step.
        self.v = None

        # The bigram stats.
        self.a = np.zeros((self.N_STATES, self.N_STATES))

        # The observation matrix.
        self.b = np.zeros((self.N_OBSERVATIONS, self.N_STATES))

        # Pointers to retrieve the topmost hypothesis.
        backptr = None

        if filename: self.init_a(filename)
        self.init_b()

    def vocalize(self, transcribed):
        bounded = '^' + transcribed + '$'
        observations = [bounded[i - 1:i + 2] for i in range(1, len(bounded) - 1)]

        states = self.viterbi(observations)
        return ''.join(states).replace('0', '').replace('A', '')

def main():
    d = HMMVocalizer()

    with open(os.path.join(BASE_DIR, 'testing.dat'), 'r') as testfile:
        for line_number, line in enumerate(testfile):

            test, real = eval(line)

            print('Observed string:')
            for observation in test:
                print(observation[1], end='')
                
            print()
            print('Real string:')
            for state in real:
                if state[0] == '0':
                    print(state[1], end='')
                else:
                    print(state, end='')
            print()

            result = d.viterbi(test)
            if result[0] == None:
                print('Invalid observation on line #%d: %s'%(line_number, result[1]))
                continue

            print('Predicted string:')
            for state in result:
                if state[0] == '0':
                    print(state[1], end='')
                else:
                    print(state, end='')
            tp, tn, fp, fn = 0, 0, 0, 0
            for predicted, true in zip(result, real):
                if predicted[0] != '0' and true[0] != '0':
                    tp += 1
                if predicted[0] == '0' and true[0] == '0':
                    tn += 1
                if predicted[0] != '0' and true[0] == '0':
                    fp += 1
                if predicted[0] == '0' and true[0] != '0':
                    fn += 1
            correct = sum(x==y for x, y in zip(real, result))
            correct_vowel = sum(x[0]==y[0] for x, y in zip(real, result) if x[0] != '0' and y[0] != '0')
            correct_consonant = sum(x[-1]==y[-1] for x, y in zip(real, result))
            print('\nCorrect states: %.2f%%\t (%d/%d)'%(correct/len(result)*100, correct, len(result)))
            print('*'*10)
            with open('test_results.csv', 'a') as t_results:
                t_results.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n'%(line_number, tp, tn, fp, fn, correct, len(result), correct_vowel, correct_consonant))


if __name__ == "__main__":
    main()
