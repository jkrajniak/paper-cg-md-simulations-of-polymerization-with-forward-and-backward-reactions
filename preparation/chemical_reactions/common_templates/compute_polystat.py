import copy
from md_libs import files_io
import sys
import argparse
import networkx as nx
import subprocess
import re
import numpy as np
import os
import multiprocessing as mp
import functools


def _args():
    parser = argparse.ArgumentParser('Put chains into groups and generate GROMACS index file')
    parser.add_argument('top')
    parser.add_argument('--trj', required=True)
    parser.add_argument('--output_prefix', default='')
    parser.add_argument('--output_index', default='chains.ndx')
    parser.add_argument('--polystat_cmd', default='gmx_mpi polystat')
    parser.add_argument('--nt', default=10, type=int)

    return parser


def compute(cmds, chain_name):
    DEVNULL = open(os.devnull, 'wb')
    polystat_cmd = subprocess.Popen(cmds + ['-o', chain_name], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=DEVNULL)
    data = polystat_cmd.communicate(input='{}\n'.format(chain_name))
    try:
        os.remove('{}.xvg'.format(chain_name))
    except IOError:
        pass
    print(chain_name)

    return data


def main():
    args = _args().parse_args()

    top = files_io.GROMACSTopologyFile(args.top)
    top.read()

    # We need graph to get the connected components.
    g = nx.Graph()
    g.add_nodes_from(top.atoms.keys())
    g.add_edges_from(top.bonds.keys())
    print('Number of nodes: {}'.format(g.number_of_nodes()))
    print('Number of edges: {}'.format(g.number_of_edges()))

    connected_components = list(nx.connected_component_subgraphs(g))
    print('Number of chains: {}'.format(len(connected_components)))
    chain_idx = 0
    chain_names = []
    chain_size = []
    with open(args.output_index, 'w') as out_index:
        for s in connected_components:
            if s.number_of_nodes() > 3:  # Do not put monomers into the groups
                nodes = sorted(s.nodes())
                out_index.write('[ chain_{} ]\n'.format(chain_idx))
                chain_names.append('chain_{}'.format(chain_idx))
                out_index.write(' '.join(map(str, nodes)))
                out_index.write('\n\n')
                chain_size.append(s.number_of_nodes())
                chain_idx += 1

    cmds = args.polystat_cmd.split() + ['-f', args.trj, '-n', args.output_index, '-b', '5000']
    output_file = '{}_ee_rg.csv'.format(args.output_prefix)
    with open(output_file, 'w') as outd:
        outd.write('# chidx ee rg n\n')
        p = mp.Pool(args.nt)
        _compute = functools.partial(compute, cmds)
        out_data = p.map(_compute, chain_names)
        for chidx, data in enumerate(out_data):
            if data[0]:
                try:
                    re_findall = re.findall(r'[0-9]+\.[0-9]+', data[0])
                    ee, rg = map(float, re_findall)
                    outd.write('{} {:.4f} {:.4f} {:.4f}\n'.format(chidx, ee, rg, chain_size[chidx]))
                except ValueError:
                    print(data, re_findall)
    print('Saved {}'.format(output_file))

if __name__ == '__main__':
    main()
