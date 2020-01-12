import copy
from md_libs import files_io
import sys
import h5py
import argparse
import os

def _args():
    parser = argparse.ArgumentParser('Update the CG topology')
    parser.add_argument('--top', required=True, help='Input CG topology')
    parser.add_argument('--conf', required=True, help='Input CG coordinate')
    parser.add_argument('--h5', required=True, help='Input H5MD file')
    parser.add_argument('--out_top', required=True, help='Output topology')
    parser.add_argument('--out_conf', required=True, help='Output coordinate')

    return parser

def main():
    args = _args().parse_args()

    top = files_io.GROMACSTopologyFile(args.top)
    top.read()

    # Remove sections
    top.atomstate = {}
    top.nonbonded_params = {}

    # Add missing bondtypes
    if 'E' not in top.bondtypes:
        top.bondtypes['E'] = {'C': {'func': 1, 'params': ['0.256395', '27244.6']}}

    if 'C' not in top.angletypes:
        top.angletypes['C'] = {}
    if 'B' not in top.angletypes['C']:
        top.angletypes['C']['B'] = {}
    top.angletypes['C']['B']['C'] = {'func': 8, 'params': ['2', '1.0']}
    top.angletypes[('C', 'B', 'C')] = {'func': 8, 'params': ['2', '1.0']}

    if 'E' not in top.dihedraltypes:
        top.dihedraltypes['E'] = {}
    if 'C' not in top.dihedraltypes['E']:
        top.dihedraltypes['E']['C'] = {}
    if 'B' not in top.dihedraltypes['E']['C']:
        top.dihedraltypes['E']['C']['B'] = {}
    top.dihedraltypes['E']['C']['B']['C'] = {'func': 8, 'params': ['0', '1.0']}
    top.dihedraltypes[('E', 'C', 'B', 'C')] = {'func': 8, 'params': ['0', '1.0']}

    for k in top.angles:
        t = tuple([top.atoms[x].atom_type for x in k])
        angletype = top.angletypes[t]
        if not ' '.join(top.angles[k]).split(';')[0].strip():
            top.angles[k] = [str(angletype['func'])] + angletype['params'] + top.angles[k]

    for k in top.dihedrals:
        t = tuple([top.atoms[x].atom_type for x in k])
        dihedraltype = top.dihedraltypes[t]
        if not ' '.join(top.dihedrals[k]).split(';')[0].strip():
            top.dihedrals[k] = [str(dihedraltype['func'])] + dihedraltype['params'] + top.dihedrals[k]

    conf = files_io.GROFile(args.conf)
    conf.read()

    h5 = h5py.File(args.h5, 'r')

    species2typename = {0: 'D', 1: 'A', 2: 'B', 3: 'C', 4: 'E', 5: 'W', 6: 'Z', 7: 'X'}
    species = h5['/particles/atoms/species/value'][-1]

    chain_names = {
        0: 'DIO',
        4: 'DIO',
        1: 'TER',
        2: 'TER',
        3: 'TER',
        5: 'H2O',
        6: 'H2O',
        7: 'DUM'
    }

    names = {
        'DIO': {('D',): ['D1'],
                ('E',): ['E1'],
            },
        'TER': {('A', 'B', 'A'): ['A1', 'B1', 'A2'],
                ('A', 'B', 'C'): ['A1', 'B1', 'C2'],
                ('C', 'B', 'A'): ['C1', 'B1', 'A2'],
                ('C', 'B', 'C'): ['C1', 'B1', 'C2']
                },
        'H2O': {('W', ): ['W1'],
                ('Z', ): ['Z1']
                }
    }


# First set correct type
    last_chain_idx = 0
    chain_id = 1
    old2new = {}
    atidx = 1
    new_atoms = {}
    conf_new_atoms = {}
    for at_id, sp in enumerate(species, 1):
        if at_id not in top.atoms:
            continue
        old2new[at_id] = atidx
        at_data = copy.copy(top.atoms[at_id])
        new_atoms[atidx] = at_data
        at_data.atom_type = species2typename[sp]
        at_data.atom_id = atidx
        if top.atoms[at_id].chain_idx != last_chain_idx:
            last_chain_idx = top.atoms[at_id].chain_idx
            at_data.chain_idx = chain_id
            chain_id += 1
        at_data.chain_name = chain_names[sp]
        conf_new_atoms[atidx] = conf.atoms[at_id]._replace(
            chain_name=chain_names[sp], chain_idx=chain_id, atom_id=atidx)
        atidx += 1

    atom_list = [new_atoms[x] for x in sorted(new_atoms)]

# Set names
    at_id = 0
    total_num = len(atom_list)
    while at_id < total_num:
        at_data = atom_list[at_id]
        name_seq = names[at_data.chain_name]
        window_size = len(name_seq.keys()[0])
        at_type_seq = tuple(x.atom_type for x in atom_list[at_id:at_id+window_size])
        for i, x in enumerate(atom_list[at_id:at_id+window_size]):
            x.name = name_seq[at_type_seq][i]
            new_atoms[x.atom_id].atom_name = x.name
            conf_new_atoms[x.atom_id] = conf_new_atoms[x.atom_id]._replace(name=x.name)
        at_id += window_size

    top.atoms = new_atoms
    conf.atoms = conf_new_atoms

    # Replace atom name C to Q (keep the type) this is because for backmapping all atoms has to be
    # unique
    for at_data in top.atoms.values():
        if at_data.name.startswith('C'):
            at_data.name = at_data.name.replace('C', 'Q')

    for at_id, at_data in conf.atoms.items():
        if at_data.name.startswith('C'):
            conf.atoms[at_id] = at_data._replace(name=at_data.name.replace('C', 'Q'))

    top.write(args.out_top, force=True)
    conf.write(args.out_conf, force=True)

if __name__ == '__main__':
    main()
