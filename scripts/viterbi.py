import argparse, sys, math
from collections import defaultdict

# author: Jonathan Yee (jyee1)

INIT, FINAL = "init", "end"

parser = argparse.ArgumentParser()
parser.add_argument('trans', type=str, help="the file to read transition probabilities from")
parser.add_argument('emit', type=str, help="the file to read emission probabilities from")
args = parser.parse_args()

# read the transition probabilities
states = set([INIT, FINAL])
trans_prob = defaultdict(lambda: defaultdict(float))
with open(args.trans) as f:
    for line in f:
        fields = line.split()
        s1, s2, prob = fields[0], fields[1], float(fields[2])
        trans_prob[s1][s2] = math.log(prob)
        states.add(s1)
        states.add(s2)

# read the emission probablities
emit_prob = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
with open(args.emit) as f:
    for line in f:
        fields = line.split()
        s, index, pixel_value, prob = fields[0], int(fields[1]), int(fields[2]), float(fields[3])
        emit_prob[s][index][pixel_value] = math.log(prob)

# read the test cases, in the same format as the original letter.data
words = []
current_word = []
for line in sys.stdin:
    fields = line.strip().split("\t")
    letter, next_id, pixels = fields[1], fields[2], fields[6:]
    pixels = [int(p) for p in pixels]
    current_word.append((letter, pixels))

    if next_id == "-1":
        words.append(current_word)
        current_word = []

def get_emit_p(s, my_pixels):
    return sum([emit_prob[s][i][my_pixels[i]] for i in xrange(len(my_pixels))]) # we work in log space!

# obs - list of pixel lists [ [1, 1, 0, ...], [0, 0, 1, ...], ... ]
# states must NOT contain INIT and FINAL
def viterbi(obs, states, trans, emit):
    V = defaultdict(lambda: defaultdict(float))
    path = {}

    # Initialize base cases (t == 0)
    for s in states:
        # print get_emit_p(s, obs[0])
        V[0][s] = trans[INIT][s] + get_emit_p(s, obs[0])
        path[s] = [s]
    # print V[0]

    # Run Viterbi for t > 0
    for t in xrange(1, len(obs)):
        newpath = {}
        for y in states:
            (prob, state) = max((V[t-1][y0] + trans[y0][y] + get_emit_p(y, obs[t]), y0) for y0 in states)
            V[t][y] = prob
            # print prob
            newpath[y] = path[state] + [y]
        # Don't need to remember the old paths
        path = newpath

    # print V[t]
    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])

correct_count = 0
total = 0
for word in words:
    # word : (letter, pixels)
    obs = [pixels for _, pixels in word]
    correct_labels = [letter for letter, _ in word]
    the_states = [s for s in states if s != INIT and s != FINAL ]
    (prob, path) = viterbi(obs, the_states, trans_prob, emit_prob)
    correct_count += sum([1 for (x, y) in zip(path, correct_labels) if x == y])
    total += len(path)
    print "MINE:", path
    print "CORR:", correct_labels
print correct_count, total
print "Overall accuracy: {}%".format(float(correct_count) * 100 / total)