import sys

for line in sys.stdin:
    fields = line.strip().split("\t")
    letter = fields[1]
    print letter