import random

lines = None
with open('transcribed.txt', 'r') as f:
    lines = [line for line in f]

random.shuffle(lines)
cutoff = int(len(lines)*.75)

with open('training.txt', 'w') as training:
    for line in lines[:cutoff]:
        training.write(line)

with open('testing.txt', 'w') as testing:
    for line in lines[cutoff:]:
        testing.write(line)
