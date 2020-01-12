import copy
from md_libs import files_io
import sys
import argparse
import networkx as nx

def _args():
    parser = argparse.ArgumentParser('Put chains into groups and generate GROMACS index file')
    parser.add_argument('top')
    parser.add_argument('output_index')

    return parser

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
    with open(args.output_index, 'w') as out_index:
        for s in connected_components:
            if s.number_of_nodes() > 3:  # Do not put monomers into the groups
                nodes = sorted(s.nodes())
                out_index.write('[ chain_{} ]\n'.format(chain_idx))
                out_index.write(' '.join(map(str, nodes)))
                out_index.write('\n\n')
                chain_idx += 1

if __name__ == '__main__':
    main()
