import h5py
import networkx as nx
import sys

h5 = h5py.File(sys.argv[1], 'r')

static_bonds = [b for b in h5['/connectivity/bonds_0'] if -1 not in b]
chem_bonds = h5['/connectivity/chem_bonds_0/value']

# Find the events when the bond is created and removed
last_num_bonds = 0
last_bonds = set()
for tstep, tb in enumerate(chem_bonds):
    bonds = {tuple(b) for b in tb if -1 not in b}
    num_bonds = len(bonds)
    if num_bonds > last_num_bonds:
        print('{} new: {}'.format(tstep, bonds - last_bonds))
    elif num_bonds < last_num_bonds:
        print('{} rm: {}'.format(tstep, last_bonds - bonds))
    if num_bonds != last_num_bonds:
        last_num_bonds = num_bonds
        last_bonds = bonds
