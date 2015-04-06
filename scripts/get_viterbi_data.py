import sys
from collections import defaultdict
import argparse

# author: Jonathan Yee (jyee1)

parser = argparse.ArgumentParser()
parser.add_argument('trans_output', type=str, help="the file to write transition probabilities to")
parser.add_argument('emit_output', type=str, help="the file to write emission probabilities to")
args = parser.parse_args()

INIT, END = "init", "end"

data = {} # (id, letter, next_id, pixels)
states = set([INIT, END])

last_state = INIT

transition_counts = defaultdict(lambda: defaultdict(int))
state_totals = defaultdict(int)
emission_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
# emission_totals = defaultdict(lambda: defaultdict(int))

for line in sys.stdin:
    fields = line.strip().split("\t")
    this_id, letter, next_id, pixels = fields[0], fields[1], fields[2], fields[6:]
    states.add(letter)

    # state_totals[letter] += 1
    transition_counts[last_state][letter] += 1
    for i in xrange(len(pixels)):
        pixel_value = pixels[i]
        emission_counts[letter][i][pixel_value] += 1
    if next_id == "-1":
        # state_totals[END] += 1
        transition_counts[letter][END] += 1
        last_state = INIT
    else:
        last_state = letter

# +1 smoothing
for s1 in states:
    for s2 in states:
        transition_counts[s1][s2] += 1
for s in states:
    state_totals[s] = sum(transition_counts[s].values())
# for pixels
for s in states:
    for i in xrange(len(emission_counts[s])): # for each pixel index
        emission_counts[letter][i][0] += 1
        emission_counts[letter][i][1] += 1

# Write transitions
with open(args.trans_output, 'w') as f:
    for s1 in states:
        for s2 in states:
            prob = float(transition_counts[s1][s2]) / state_totals[s1]
            # s1 s2 prob
            f.write("{} {} {}".format(s1, s2, prob) + "\n")

# Write emissions
with open(args.emit_output, 'w') as f:
    for s in states:
        for i in xrange(len(emission_counts[s])):
            for pixel_value in emission_counts[s][i]:
                prob = float(emission_counts[s][i][pixel_value]) / sum(emission_counts[s][i].values())
                # state index pixel_value prob
                f.write("{} {} {} {}".format(s, i, pixel_value, prob) + "\n")