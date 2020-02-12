import h5py
import sys

h5 = h5py.File(sys.argv[1], 'r')

forces = h5['/particles/atoms/force/value']

