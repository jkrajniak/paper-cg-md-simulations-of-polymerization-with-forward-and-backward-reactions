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

Partially this file is stolen from https://github.com/pdebuyl/md_tools
and modified but the original file has the following copyright header:

 Copyright 2014 Pierre de Buyl

 This file is part of md_tools

 md_tools is free software and is licensed under the modified BSD license (see
 LICENSE file).
"""

import numpy as np
cimport numpy as np
from libc.math cimport sqrt, floor
cimport cython

def compute_rdf(r, L, N, cutoff):
    """
    Compute the radial distribution function (rdf). The number of rdf
    components, N_rdf, is 1 for a single species system, n_idx*(n_idx+1)/2 for a
    multi-species system where n_idx=n_species if state is not specified and
    n_idx=sum(n_state) if state is specified.

    Arguments
    ---------

    r: [N,3] array of positions
    L: [3] sides of a cuboid box
    N: nbins

    Returns
    -------

    dx, all_rdf, count
    dx is the radius step
    all_rdf is a [N_rdf,N]
    count is a [N_rdf] array

    """
    cdef int i, n_rdf, n_idx
    cdef double[3] cy_L
    for i in range(3):
        cy_L[i] = L[i]

    if cutoff == -1:
        x_max = np.min(L)/2.
    else:
        x_max = cutoff
    dx = x_max/N

    result = _compute_rdf(r, cy_L, N, dx)
    return dx, np.asarray(result)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef _compute_rdf(double[:, ::1] r, double[3] L, int N, double dx):
    cdef int i, j, coord, idx, si, sj, rdf_idx, n_idx
    cdef double dist
    cdef double dist_sqr
    cdef double inv_dx = 1./dx
    cdef double x_max_sqr = (N*dx)**2
    cdef double pi = np.pi
    cdef double k

    cdef double[::1] result = np.zeros(N)

    for i in range(r.shape[0]):
        si = 0
        for j in range(i+1, r.shape[0]):
            dist_sqr = 0.0
            for coord in range(3):
                dist = r[i,coord]-r[j,coord]
                if dist<-L[coord]/2.:
                    dist += L[coord]
                elif dist>L[coord]/2.:
                    dist -= L[coord]
                dist_sqr += dist**2
            if dist_sqr <= x_max_sqr:
                idx = int(floor(sqrt(dist_sqr)*inv_dx))
                result[idx] += 1

    k = 2.0*pi
    for i in range(result.shape[0]):
        result[i] /= (k*((i+0.5)*dx)**2)

    return result
