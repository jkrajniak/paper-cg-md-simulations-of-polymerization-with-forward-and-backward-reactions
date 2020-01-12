#!/usr/bin/env python
"""
Copyright (C) 2017 Jakub Krajniak <jkrajniak@gmail.com>

This file is distributed under free software licence:
you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import h5py
import numpy as np

from matplotlib import pyplot as plt

import _rdf


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument('h5')
    parser.add_argument('--bins', default=100, type=int)
    parser.add_argument('-n', default=None, help='Index file')
    parser.add_argument('-b', default=0, type=int)
    parser.add_argument('-e', default=-1, type=int)
    parser.add_argument('--cutoff', default=-1, type=float)

    return parser.parse_args()


def main():
    args = _args()
    h5 = h5py.File(args.h5, 'r')

    pids = None
    npart = None
    if args.n:
        with open(args.n, 'r') as findex:
            pids = map(int, ' '.join(findex.readlines()).split())
            npart = len(pids)

    pos = h5['/particles/atoms/position/value']
    ids = h5['/particles/atoms/id/value']
    L = h5['/particles/atoms/box/edges']
    result = np.zeros(args.bins)
    frames = (pos.shape[0] if args.e == -1 else args.e) - args.b
    for i in xrange(args.b, pos.shape[0] if args.e == -1 else args.e):
        idd = ids[i]
        p = pos[i][np.where(idd != -1)[0]]
        if pids:
            pp = p[pids]
        else:
            pp = p
            npart = pp.shape[0]
        dx, tmp_r = _rdf.compute_rdf(np.asarray(pp, dtype=np.double), L, args.bins, args.cutoff)
        result += tmp_r

    phi = npart/(L[0]*L[1]*L[2])
    norm = dx*phi*frames*npart
    plt.plot(dx*(np.arange(0, args.bins)+0.5), result/norm)
    plt.show()

if __name__ == '__main__':
    main()

