import sys

for line in sys.stdin:
    fields = line.strip().split("\t")
    pixels = fields[6:]
    letter = fields[1]
    print letter
    stars = [['*' if p == '1' else ' ' for p in pixels[i*8:(i+1)*8]] for i in xrange(16)]
    rows = ["".join(row) for row in stars]
    print "\n".join(rows)