import h5py
import numpy as np
import sys

h5 = h5py.File(sys.argv[1], 'r')

particle_pairs = []
for i in range(1000):
    particle_pairs.append((1000+3*i, 4000+2*i))
    particle_pairs.append((1000+3*i+2, 4000+2*i+1))

print(len(particle_pairs))
print(particle_pairs[:10])

pos = h5['/particles/atoms/position/value']
img = h5['/particles/atoms/image/value']
if 'value' in h5['/particles/atoms/box/edges']:
    box = np.array(h5['/particles/atoms/box/edges/value'][-1])
else:
    box = np.array(h5['/particles/atoms/box/edges'])

distances = []

print(pos.shape[0])
for T in range(0, pos.shape[0]):
    tmp_d = []
    for a_id, d_id in particle_pairs:
        p_a = pos[T][a_id] + np.array(img[T][a_id])*box
        p_d = pos[T][d_id] + np.array(img[T][d_id])*box
        d = p_d - p_a
        if np.sqrt(d.dot(d)) > 0.8:
            continue
        tmp_d.append(np.sqrt(d.dot(d)))
    distances.append((T, np.average(tmp_d)))
    print(T)
np.savetxt('distances_a_d.csv', distances)
