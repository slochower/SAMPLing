import sys
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',
                filename='log.convergence'+sys.argv[1], level=log.DEBUG)
import parmed as pmd
import pytraj as pt
import numpy as np
import paprika
log.debug('version: '+paprika.__version__)
from paprika import align
from paprika import tleap
from paprika import dummy
from paprika import restraints
from paprika import analysis
from paprika import amber
from paprika import utils
import os
import sys
import shutil
import re

conf_name = 'CB8-G3-'+sys.argv[1]
fractions = np.arange(0.01, 1.01, 0.01)
#fractions = np.array([1.0])

### Some initial CB8 stuff

# Anchor atoms
host_anch  = [':HST@C2', ':HST@C8', ':HST@C16']
guest_anch = [':GST@C17', ':GST@N2']
dummy_anch = [':DM1', ':DM2', ':DM3']

# Guest restraint details
attach_fractions = [0.0000, 0.0040, 0.0080, 0.0160, 0.0240, 0.0400, 0.0550, 0.0865, 0.1180, 0.1810, 0.2440, 0.3700, 0.4960, 0.7480, 1.0000]
num_attach_windows = len(attach_fractions)
attach_dist_fc = 5.0 # kcal/mol-Angstrom**2
attach_dist_target = 6.0 # Angstrom
pull_dist_target = 24.0 # Angstrom
pull_dist_incr = 0.4 # Angstrom
num_pull_windows = int(1. + (pull_dist_target-attach_dist_target)/pull_dist_incr )
attach_ang_fc = 100 # kcal/mol-rad**2
attach_ang_target = 180.0 # degrees
pull_ang_target = 180.0 # degrees
num_release_windows = 0


# Load pmd AmberParm
prmtop = conf_name+'/windows/a000/vac.prmtop'
rst7 = conf_name+'/windows/a000/vac.rst7'
pmd_parm = pmd.amber.AmberParm(prmtop, xyz=rst7)

# Setup guest restraints
guest_rests = []

# Guest Translational Distance
guest_rests.append(restraints.DAT_restraint())
guest_rests[-1].auto_apr = False
guest_rests[-1].amber_index = True
guest_rests[-1].topology = pmd_parm
guest_rests[-1].mask1 = dummy_anch[0]
guest_rests[-1].mask2 = guest_anch[0]
guest_rests[-1].attach['target'] = attach_dist_target
guest_rests[-1].attach['fraction_list'] = attach_fractions
guest_rests[-1].attach['fc_final'] = attach_dist_fc
guest_rests[-1].pull['fc'] = attach_dist_fc
guest_rests[-1].pull['target_initial'] = attach_dist_target
guest_rests[-1].pull['target_final'] = pull_dist_target
guest_rests[-1].pull['num_windows'] = num_pull_windows
guest_rests[-1].initialize()

# Guest Translational Angle
guest_rests.append(restraints.DAT_restraint())
guest_rests[-1].auto_apr = False
guest_rests[-1].amber_index = True
guest_rests[-1].topology = pmd_parm
guest_rests[-1].mask1 = dummy_anch[1]
guest_rests[-1].mask2 = dummy_anch[0]
guest_rests[-1].mask3 = guest_anch[0]
guest_rests[-1].attach['target'] = attach_ang_target
guest_rests[-1].attach['fraction_list'] = attach_fractions
guest_rests[-1].attach['fc_final'] = attach_ang_fc
guest_rests[-1].pull['fc'] = attach_ang_fc
guest_rests[-1].pull['target_initial'] = pull_ang_target
guest_rests[-1].pull['target_final'] = pull_ang_target
guest_rests[-1].pull['num_windows'] = num_pull_windows
guest_rests[-1].initialize()

# Guest Orientational Angle
guest_rests.append(restraints.DAT_restraint())
guest_rests[-1].auto_apr = False
guest_rests[-1].amber_index = True
guest_rests[-1].topology = pmd_parm
guest_rests[-1].mask1 = dummy_anch[0]
guest_rests[-1].mask2 = guest_anch[0]
guest_rests[-1].mask3 = guest_anch[1]
guest_rests[-1].attach['target'] = attach_ang_target
guest_rests[-1].attach['fraction_list'] = attach_fractions
guest_rests[-1].attach['fc_final'] = attach_ang_fc
guest_rests[-1].pull['fc'] = attach_ang_fc
guest_rests[-1].pull['target_initial'] = pull_ang_target
guest_rests[-1].pull['target_final'] = pull_ang_target
guest_rests[-1].pull['num_windows'] = num_pull_windows
guest_rests[-1].initialize()

# Make window list
window_list = restraints.create_window_list(guest_rests)

# Collect Data
data = np.zeros((2, len(fractions), 10))
for fraction_index, fraction in enumerate(fractions):

    fecalc = analysis.fe_calc()
    fecalc.prmtop = 'vac.prmtop'
#    fecalc.trajectory = [
#                         'prod.001.nc', 'prod.002.nc', 'prod.003.nc', 'prod.004.nc',
#                         'prod.005.nc', 'prod.006.nc', 'prod.007.nc', 'prod.008.nc',
#                         'prod.009.nc', 'prod.010.nc',
#                         ]
    fecalc.trajectory = 'prod.*.nc'
    fecalc.path = os.path.join(conf_name, 'windows')
    fecalc.restraint_list = guest_rests
    fecalc.methods = ['mbar-block', 'ti-block']
    #fecalc.methods = ['mbar-block']
    fecalc.quicker_ti_matrix = True
    fecalc.bootcycles = 1000
    fecalc.collect_data(fraction=fraction)
    fecalc.compute_free_energy()
    fecalc.compute_ref_state_work([guest_rests[0],guest_rests[1],None,None,guest_rests[2],None])

    for meth_idx, method in enumerate(fecalc.methods):
        data[meth_idx, fraction_index, 0] = fraction
        data[meth_idx, fraction_index, 1] = fecalc.results['attach'][method]['fe']
        data[meth_idx, fraction_index, 2] = fecalc.results['attach'][method]['sem']
        data[meth_idx, fraction_index, 3] = fecalc.results['attach'][method]['n_frames']
    
        data[meth_idx, fraction_index, 4] = fecalc.results['pull'][method]['fe']
        data[meth_idx, fraction_index, 5] = fecalc.results['pull'][method]['sem']
        data[meth_idx, fraction_index, 6] = fecalc.results['pull'][method]['n_frames']
    
        data[meth_idx, fraction_index, 7] = fecalc.results['ref_state_work']
    
        fe = data[meth_idx, fraction_index, 1] + data[meth_idx, fraction_index, 4] + data[meth_idx, fraction_index, 7]
        fe_sem = np.sqrt(data[meth_idx, fraction_index, 2]**2 + data[meth_idx, fraction_index, 5]**2)
        data[meth_idx, fraction_index, 8] = fe
        data[meth_idx, fraction_index, 9] = fe_sem
        log.info("{} {} {} {:2.3f} ({:2.3f})".format(conf_name, method, fraction, fe, fe_sem))

for meth_idx, method in enumerate(['mbar-block', 'ti-block']):    
    np.savetxt('{}-{}-fe-all.log'.format(conf_name, method), data[meth_idx])
