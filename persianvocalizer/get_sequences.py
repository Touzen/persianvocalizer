import random

hiddens = ('a', 'o', 'e', 'è')
for f_name in ('testing', 'training'):
    with open(f_name + '.dat', 'w') as output:
        with open(f_name + '.txt', 'r') as transcribed:
            for line_num, line in enumerate(transcribed):
                if random.randint(0, 30) == 4:
                    print('Processing line number %d: %s...'%(line_num, line[:min(len(line), 50)].strip()))

                line = line.strip()
                line = '^' + line + '$'
                observations = []
                states = []

                # Add alefs
                index = 1
                while index < len(line)-1:
                    if line[index] not in hiddens and line[index] != 'i':
                        index += 1
                        continue
                    else:
                        if line[index-1] in (' ', '^'):
                            line = line[:index] + 'A' + line[index:]
                    index += 1
                
                # Extract the observations and states
                line_length = len(line)
                for index in range(1, line_length - 1):
                    if line[index] in hiddens:
                        continue

                    observation = ''

                    first_char = ''
                    for i in range(0, index):
                        char = line[i]
                        if char not in hiddens:
                            first_char = char
                            
                    observation += first_char
                        
                    for i in range(index, line_length):
                        char = line[i]
                        if char not in hiddens:
                            if char == 'u':
                                char = 'v'
                            observation += char
                        if len(observation) >= 3:
                            break

                    state_char = line[index-1]
                    if state_char not in hiddens:
                        state_char = '0'
                    state = state_char + line[index]
                    
                    observations.append(observation)
                    states.append(state)
                output.write(str((observations, states))+'\n')
