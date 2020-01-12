import h5py
import sys


h5 = h5py.File(sys.argv[1], 'r')

all_bonds = [tuple(b) for b in h5['/connectivity/bonds_0'] if -1 not in b]
all_bonds.extend([tuple(b) for b in h5['/connectivity/chem_bonds_0/value'][-1] if -1 not in b])
all_bonds.extend([tuple(reversed(b)) for b in all_bonds[:]])
print('Bonds {}'.format(len(all_bonds)))
wrong_angle = []
wrong_dihedral = []
try:
    angles = [tuple(a) for a in h5['/connectivity/dynamic_angles_0/value'][-1] if -1 not in a]
    dihedrals = [tuple(a) for a in h5['/connectivity/dynamic_dihedrals_0/value'][-1] if -1 not in a]

    print('Angles {}'.format(len(angles)))
    print('Dihedrals {}'.format(len(dihedrals)))

    for a in angles:
        a1, a1r = tuple(a[:2]), tuple(reversed(a[:2]))
        a2, a2r = tuple(a[1:]), tuple(reversed(a[1:]))
        if a1 not in all_bonds and a1r not in all_bonds:
            wrong_angle.append(a)
        if a2 not in all_bonds and a2r not in all_bonds:
            wrong_angle.append(a)

    for d in dihedrals:
        d1, d1r = tuple(d[:2]), tuple(reversed(d[:2]))
        d2, d2r = tuple(d[1:3]), tuple(reversed(d[1:3]))
        d3, d3r = tuple(d[2:]), tuple(reversed(d[2:]))
        if d1 not in all_bonds and d1r not in all_bonds:
            wrong_dihedral.append(d)
        if d2 not in all_bonds and d2r not in all_bonds:
            wrong_dihedral.append(d)
        if d3 not in all_bonds and d3r not in all_bonds:
            wrong_dihedral.append(d)
except:
    to_check = map(int, sys.argv[2].split('-'))
    if len(to_check) == 3:
        a1, a1r = tuple(to_check[:2]), tuple(reversed(to_check[:2]))
        a2, a2r = tuple(to_check[1:]), tuple(reversed(to_check[1:]))
        if a1 not in all_bonds and a1r not in all_bonds:
            wrong_angle.append(to_check)
        if a2 not in all_bonds and a2r not in all_bonds:
            wrong_angle.append(to_check)
    elif len(to_check) == 4:
        d = to_check
        d1, d1r = tuple(d[:2]), tuple(reversed(d[:2]))
        d2, d2r = tuple(d[1:3]), tuple(reversed(d[1:3]))
        d3, d3r = tuple(d[2:]), tuple(reversed(d[2:]))
        if d1 not in all_bonds and d1r not in all_bonds:
            wrong_dihedral.append(d)
        if d2 not in all_bonds and d2r not in all_bonds:
            wrong_dihedral.append(d)
        if d3 not in all_bonds and d3r not in all_bonds:
            wrong_dihedral.append(d)


print('Wrong angles: {}'.format(len(wrong_angle)))
print('Wrong dihedrals: {}'.format(len(wrong_dihedral)))
if wrong_dihedral or wrong_angle:
    print wrong_angle
    print wrong_dihedral
    import IPython; IPython.embed()
