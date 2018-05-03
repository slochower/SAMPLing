import glob as glob
import os as os
import numpy as np
import sys as sys

import logging
logging.basicConfig(
    filename='G6-analyze.log',
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=logging.DEBUG)
logging.info('Started logging...')

import pytraj as pt
import parmed as pmd
import paprika
logging.info(paprika.__version__)
from paprika.restraints import DAT_restraint
from paprika.analysis import fe_calc


# Setup the restraints based on the `jupyter notebook`s.
dummy_anchors = [':3', ':4', ':5']
host_anchors = [':1@C26', ':1@C18', ':1@C8']
guest_anchors = [':2@C1', ':2@C3']

attach_string = '0.00 0.40 0.80 1.60 2.40 4.00 5.50 8.65 11.80 ' \
                '18.10 24.40 37.00 49.60 74.80 100.00'
pull_string = '0.00 0.40 0.80 1.20 1.60 2.00 2.40 2.80 3.20 3.60 4.00 ' \
              '4.40 4.80 5.20 5.60 6.00 6.40 6.80 7.20 7.60 8.00 8.40 ' \
              '8.80 9.20 9.60 10.00 10.40 10.80 11.20 11.60 12.00 12.40 ' \
              '12.80 13.20 13.60 14.00 14.40 14.80 15.20 15.60 16.00 16.40 ' \
              '16.80 17.20 17.60 18.00'

attach_fractions = [float(i) / 100 for i in attach_string.split()]
windows = [len(attach_fractions), len(pull_string.split()), 0]
paths = glob.glob(
    os.path.normpath(
        os.path.join('./OA-G3-0', 'AMBER', 'APR', 'windows', '*')))
window_list = [os.path.basename(i) for i in paths]

# Setup the fractions for SAMPLing convergence...
fractions = np.arange(0.01, 1.01, 0.01)

# Run (for now) over all the G3 complexes...
# g3_complexes = sorted(glob.glob('OA-G3-*'))
# g3_complexes = [i for i in g3_complexes if os.path.isdir(i)]
# 
# for complex_index, complx in enumerate(sorted(g3_complexes)):
#     print(complx)
#     if os.path.isfile(complx + '-fe-all.log'):
#         print('Skipping...')
#         continue
#     traj = pt.load(
#         os.path.join(complx, 'AMBER', 'solvate.rst7'),
#         os.path.join(complx, 'AMBER', 'solvate.prmtop'))
# 
#     pull_initial = pt.distance(traj, ' '.join(
#         [dummy_anchors[0], guest_anchors[0]]))[0]
# 
#     pull_distances = [float(i) + pull_initial for i in pull_string.split()]
# 
#     guest_restraint_atoms = [
#         [dummy_anchors[0], guest_anchors[0]],
#         [dummy_anchors[1], dummy_anchors[0], guest_anchors[0]],
#         [dummy_anchors[0], guest_anchors[0], guest_anchors[1]],
#     ]
# 
#     guest_restraint_targets = [pull_initial, 180.0, 180.0]
#     guest_restraint_target_final = [pull_distances[-1], 180.0, 180.0]
#     guest_restraint_distance_fc = 5.0  # kcal/mol-A**2
#     guest_restraint_angle_fc = 100.0  # kcal/mol-rad**2
# 
#     hg = pmd.load_file(
#         os.path.join(complx, 'AMBER', 'solvate.prmtop'),
#         os.path.join(complx, 'AMBER', 'solvate.rst7'),
#         structure=True)
# 
#     guest_restraints = []
#     for index, atoms in enumerate(guest_restraint_atoms):
#         if len(atoms) > 2:
#             angle = True
#         else:
#             angle = False
#         this = DAT_restraint()
#         this.auto_apr = True
#         this.amber_index = True
#         this.topology = hg
#         this.mask1 = atoms[0]
#         this.mask2 = atoms[1]
#         if angle:
#             this.mask3 = atoms[2]
#             this.attach['fc_final'] = guest_restraint_angle_fc
#         else:
#             this.attach['fc_final'] = guest_restraint_distance_fc
#         this.attach['target'] = guest_restraint_targets[index]
#         this.attach['fraction_list'] = attach_fractions
# 
#         this.pull['target_final'] = guest_restraint_target_final[index]
#         this.pull['num_windows'] = windows[1]
#         this.initialize()
# 
#         guest_restraints.append(this)
# 
#     structure = pt.load(
#         os.path.join(complx, 'AMBER', 'APR', 'windows', 'a000',
#                      'solvate.rst7'),
#         os.path.join(complx, 'AMBER', 'APR', 'windows', 'a000',
#                      'solvate.prmtop'))
# 
#     stripped = structure.strip(':WAT,:Na+,:Cl-')
# 
#     data = np.zeros((len(fractions), 8))
#     for fraction_index, fraction in enumerate(fractions):
# 
#         fecalc = fe_calc()
#         fecalc.prmtop = stripped.topology
#         fecalc.trajectory = 'prod.*.nc'
#         fecalc.path = os.path.join(complx, 'AMBER', 'APR', 'windows')
#         fecalc.restraint_list = guest_restraints
#         fecalc.collect_data(fraction=fraction)
#         fecalc.compute_free_energy()
# 
#         data[fraction_index, 0] = fraction
#         data[fraction_index, 1] = fecalc.results['attach']['mbar-block']['fe']
#         data[fraction_index, 2] = fecalc.results['attach']['mbar-block']['sem']
#         data[fraction_index, 3] = fecalc.results['attach']['mbar-block'][
#             'n_frames']
# 
#         data[fraction_index, 4] = fecalc.results['pull']['mbar-block']['fe']
#         data[fraction_index, 5] = fecalc.results['pull']['mbar-block']['sem']
#         data[fraction_index, 6] = fecalc.results['pull']['mbar-block'][
#             'n_frames']
# 
#         fecalc.compute_ref_state_work([
#             guest_restraints[0], guest_restraints[1], None, None,
#             guest_restraints[2], None
#         ])
# 
#         data[fraction_index, 7] = fecalc.results['ref_state_work']
# 
#         # print(f"{complx} {fraction}")
#         # print(f"{fecalc.results['attach']['mbar-block']['fe']:2.3f} ± {fecalc.results['attach']['mbar-block']['sem']:2.3f}")
#         # print(f"{fecalc.results['pull']['mbar-block']['fe']:2.3f} ± {fecalc.results['pull']['mbar-block']['sem']:2.3f}")
#         fe = data[fraction_index, 1] + data[fraction_index,
#                                             4] + data[fraction_index, 7]
#         fe_sem = np.sqrt(
#             data[fraction_index, 2]**2 + data[fraction_index, 5]**2)
#         print(f"{complx} {fraction} {fe:2.3f} ± {fe_sem:2.3f}")
# 
#     np.savetxt('{}-fe-all.log'.format(complx), data)

guest_anchors = [':2@C6', ':2@C1']

attach_string = '0.00 0.40 0.80 1.60 2.40 4.00 5.50 8.65 11.80 ' \
                '18.10 24.40 37.00 49.60 74.80 100.00'
pull_string = '0.00 0.40 0.80 1.20 1.60 2.00 2.40 2.80 3.20 3.60 4.00 ' \
              '4.40 4.80 5.20 5.60 6.00 6.40 6.80 7.20 7.60 8.00 8.40 ' \
              '8.80 9.20 9.60 10.00 10.40 10.80 11.20 11.60 12.00 12.40 ' \
              '12.80 13.20 13.60 14.00 14.40 14.80 15.20 15.60 16.00 16.40 ' \
              '16.80 17.20 17.60 18.00'

attach_fractions = [float(i) / 100 for i in attach_string.split()]
windows = [len(attach_fractions), len(pull_string.split()), 0]
paths = glob.glob(
    os.path.normpath(
        os.path.join('./OA-G3-0', 'AMBER', 'APR', 'windows', '*')))
window_list = [os.path.basename(i) for i in paths]

# Setup the fractions for SAMPLing convergence...
g6_complexes = sorted(glob.glob('OA-G6-*'))
g6_complexes = [i for i in g6_complexes if os.path.isdir(i)]
print(g6_complexes)

for complex_index, complx in enumerate(g6_complexes):
    print(complx)
    if os.path.isfile(complx + '-fe-all.log'):
        print('Skipping...')
        continue
    traj = pt.load(
        os.path.join(complx, 'AMBER', 'solvate.rst7'),
        os.path.join(complx, 'AMBER', 'solvate.prmtop'))

    pull_initial = pt.distance(traj, ' '.join(
        [dummy_anchors[0], guest_anchors[0]]))[0]

    pull_distances = [float(i) + pull_initial for i in pull_string.split()]

    guest_restraint_atoms = [
        [dummy_anchors[0], guest_anchors[0]],
        [dummy_anchors[1], dummy_anchors[0], guest_anchors[0]],
        [dummy_anchors[0], guest_anchors[0], guest_anchors[1]],
    ]

    guest_restraint_targets = [pull_initial, 180.0, 180.0]
    guest_restraint_target_final = [pull_distances[-1], 180.0, 180.0]
    guest_restraint_distance_fc = 5.0  # kcal/mol-A**2
    guest_restraint_angle_fc = 100.0  # kcal/mol-rad**2

    hg = pmd.load_file(
        os.path.join(complx, 'AMBER', 'solvate.prmtop'),
        os.path.join(complx, 'AMBER', 'solvate.rst7'),
        structure=True)

    guest_restraints = []
    for index, atoms in enumerate(guest_restraint_atoms):
        if len(atoms) > 2:
            angle = True
        else:
            angle = False
        this = DAT_restraint()
        this.auto_apr = True
        this.amber_index = True
        this.topology = hg
        this.mask1 = atoms[0]
        this.mask2 = atoms[1]
        if angle:
            this.mask3 = atoms[2]
            this.attach['fc_final'] = guest_restraint_angle_fc
        else:
            this.attach['fc_final'] = guest_restraint_distance_fc
        this.attach['target'] = guest_restraint_targets[index]
        this.attach['fraction_list'] = attach_fractions

        this.pull['target_final'] = guest_restraint_target_final[index]
        this.pull['num_windows'] = windows[1]
        this.initialize()

        guest_restraints.append(this)

    structure = pt.load(
        os.path.join(complx, 'AMBER', 'APR', 'windows', 'a000',
                     'solvate.rst7'),
        os.path.join(complx, 'AMBER', 'APR', 'windows', 'a000',
                     'solvate.prmtop'))

    stripped = structure.strip(':WAT,:Na+,:Cl-')

    data = np.zeros((len(fractions), 8))
    for fraction_index, fraction in enumerate(fractions):

        fecalc = fe_calc()
        fecalc.prmtop = stripped.topology
        fecalc.trajectory = 'prod.*.nc'
        fecalc.path = os.path.join(complx, 'AMBER', 'APR', 'windows')
        fecalc.restraint_list = guest_restraints
        fecalc.collect_data(fraction=fraction)
        fecalc.compute_free_energy()

        data[fraction_index, 0] = fraction
        data[fraction_index, 1] = fecalc.results['attach']['mbar-block']['fe']
        data[fraction_index, 2] = fecalc.results['attach']['mbar-block']['sem']
        data[fraction_index, 3] = fecalc.results['attach']['mbar-block'][
            'n_frames']

        data[fraction_index, 4] = fecalc.results['pull']['mbar-block']['fe']
        data[fraction_index, 5] = fecalc.results['pull']['mbar-block']['sem']
        data[fraction_index, 6] = fecalc.results['pull']['mbar-block'][
            'n_frames']

        fecalc.compute_ref_state_work([
            guest_restraints[0], guest_restraints[1], None, None,
            guest_restraints[2], None
        ])

        data[fraction_index, 7] = fecalc.results['ref_state_work']

        fe = data[fraction_index, 1] + data[fraction_index,
                                            4] + data[fraction_index, 7]
        fe_sem = np.sqrt(
            data[fraction_index, 2]**2 + data[fraction_index, 5]**2)
        print(f"{complx} {fraction} {fe:2.3f} ± {fe_sem:2.3f}")

    np.savetxt('{}-fe-all.log'.format(complx), data)
