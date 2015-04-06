import sys

# author: Jonathan Yee (jyee1)

for line in sys.stdin:
    fields = line.strip().split("\t")
    pixels = fields[6:]
    print ','.join(pixels)