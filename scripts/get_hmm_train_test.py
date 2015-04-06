import argparse, sys, math, random
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('train', type=str, help="the file to write training data to")
parser.add_argument('test', type=str, help="the file to write test data to")
parser.add_argument('N', type=int, help="the number of test words")
args = parser.parse_args()

words = []
current_word = []
for line in sys.stdin:
    fields = line.strip().split("\t")
    letter, next_id, pixels = fields[1], fields[2], fields[6:]
    pixels = [int(p) for p in pixels]
    current_word.append((letter, pixels, line))

    if next_id == "-1":
        words.append(current_word)
        current_word = []

random.shuffle(words)

test = words[:args.N]
train = words[args.N:]

with open(args.train, 'w') as f:
    for word in train:
        for _, _, line in word:
            f.write(line)

with open(args.test, 'w') as f:
    for word in test:
        for _, _, line in word:
            f.write(line)
