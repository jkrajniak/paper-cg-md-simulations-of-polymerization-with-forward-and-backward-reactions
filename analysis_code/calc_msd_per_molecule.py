import argparse
import functools
import numpy as np
import os
import subprocess
import multiprocessing as mp

from md_libs import files_io



def calc_msd(traj_file, output_prefix, args):
    atom_ids, mol_id = args
    current = mp.current_process()
    rank = current._identity[0]
    index_file = 'tmp_water_{}.ndx'.format(rank)
    with open(index_file, 'w') as iw:
        iw.write('[ H2O ]\n')
        iw.write(' '.join(map(str, atom_ids)))
        iw.write('\n')

    DEVNULL = open(os.devnull, 'wb')

    msd_cmd = subprocess.Popen(['gmx_mpi', 'msd', '-f', traj_file, '-n', index_file, '-o', '{}msd_{}.xvg'.format(output_prefix, mol_id)], stdout=subprocess.PIPE, stderr=DEVNULL)
    data = msd_cmd.stdout.readlines()
    ret = [mol_id, -1, -1]
    if data:
        msd_part = data[-1].split()
        msd_data = map(float, [msd_part[2], msd_part[4].replace(')', '')])
        ret = [mol_id, msd_data[0], msd_data[1]]
    print(ret)
    os.remove(index_file)
    return ret

def _args():
    parser = argparse.ArgumentParser('Calculate MSD for individual water molecules')
    parser.add_argument('--in_top', help='.top file', required=True)
    parser.add_argument('--trj', help='Trajectory file', required=True)
    parser.add_argument('--nt', default=4, type=int, help='Number of processes')
    parser.add_argument('--mol_name', help='Water molecule name', required=True)
    parser.add_argument('--mol_size', default=3, type=int, help='Size of water molecule')
    parser.add_argument('--output', default='msd_data', help='Output file')
    parser.add_argument('--output_prefix', default='', help='Prefix for files')

    return parser

def main():
    args = _args().parse_args()

    top = files_io.GROMACSTopologyFile(args.in_top)
    top.read()

    water_molecules = [x for x in sorted(top.atoms) if top.atoms[x].chain_name == args.mol_name]

    atom_ids = [(water_molecules[i:i+args.mol_size], mol_id)
                for mol_id, i in enumerate(range(0, len(water_molecules), args.mol_size))]

    p = mp.Pool(args.nt)

    _calc_msd = functools.partial(calc_msd, args.trj, args.output_prefix)
    mol_msd_data = p.map(_calc_msd, atom_ids)

    np.savetxt('{}{}'.format(args.output_prefix, args.output), mol_msd_data, header='mol_id D +/-')


if __name__ == '__main__':
    main()
