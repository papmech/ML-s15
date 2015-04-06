import sys

# author: Jonathan Yee (jyee1)

for line in sys.stdin:
    fields = line.strip().split("\t")
    letter = fields[1]
    print letter