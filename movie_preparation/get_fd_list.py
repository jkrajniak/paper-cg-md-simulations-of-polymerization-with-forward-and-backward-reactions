import cPickle
import sys

host_id = int(sys.argv[2])

i = 401
for p in range(101, 401):
    if p % 3 in [2, 1]:
        print(p, i)
        i += 1
