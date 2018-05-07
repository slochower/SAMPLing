import logging as log
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',
                filename='log.execute', level=log.DEBUG)

import numpy as np
import paprika
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
import subprocess as sp
import re

#Run Simulations

# Simulation steps per iteration
itr_nstlim = 50000

# Original Workdir (remember, this happens in $TMPDIR)
oworkdir = os.environ['PBS_O_WORKDIR']
tmpdir = os.environ['TMPDIR']

# Loop of restart iterations
for itr in range(3):

    # Strings for restart iterations
    prev = "{:03.0f}".format(itr)
    curr = "{:03.0f}".format(itr+1)

    log.debug('----- prev :'+prev+' cur: '+curr+' -----')

    # If first time through, create simulation class and minimize
    if itr == 0:
        sim = amber.Simulation()
        sim.executable = 'pmemd.cuda'
        #sim.CUDA_VISIBLE_DEVICES = 6
        sim.path = '.'
        sim.topology = os.path.join(oworkdir,'solvated.prmtop')
        sim.prefix = 'minimize'
        sim.inpcrd = os.path.join(oworkdir,'solvated.rst7')
        sim.ref = os.path.join(oworkdir,'solvated.rst7')
        sim.config_pbc_min()
        sim.cntrl['maxcyc'] = 500
        sim.cntrl['ncyc'] = 400
        sim.cntrl['cut'] = 9.0
        sim.cntrl['ntr'] = 1
        sim.cntrl['restraint_wt'] = 50.0
        sim.cntrl['restraintmask'] = "'@DUM'"
        # This might be an overwrite run, so check if minimize is done already
        if not os.path.isfile( os.path.join(oworkdir, sim.restart) ):
            sim.run()
            sp.call(['rsync','-au', tmpdir+'/', oworkdir+'/'])
        
        # Run Equilibration ... if we terminate early due to
        # box size changes, continue on from restart
        sim.config_pbc_md()
        sim.executable = 'pmemd.cuda'
        sim.cntrl['nstlim'] = 500000
        sim.cntrl['ntwx'] = 0
        sim.cntrl['ntwprt'] = 196
        sim.cntrl['ntwr'] = 250
        sim.cntrl['cut'] = 9.0
        i = 0
        sim.prefix = 'equil.'+str(i)
        sim.inpcrd = os.path.join(oworkdir,'minimize.rst7')
        sim.ref = os.path.join(oworkdir,'solvated.rst7')
        # Run equil loop until we complete a full equil cycle.
        # Then copy the final rst7 to 'equil.rst7'
        while not os.path.isfile(os.path.join(oworkdir,'equil.rst7')) and i < 10:
            if not os.path.isfile(os.path.join(oworkdir,sim.inpcrd)):
                raise Exception('Problem encountered with running equilibration')
            sim.run(fail_ok=True)
            with open('equil.'+str(i)+'.out') as f:
                for line in f.readlines():
                    if re.search(' TIMINGS', line):
                        shutil.copy(sim.restart, 'equil.rst7')
            sp.call(['rsync','-au', tmpdir+'/', oworkdir+'/'])
            i += 1
            sim.prefix = 'equil.'+str(i)
            sim.inpcrd = os.path.join(oworkdir, 'equil.'+str(i-1)+'.rst7')
            sim.ref = os.path.join(oworkdir, 'solvated.rst7')

    # Setup production MD
    if itr == 0:
        sim.config_pbc_md()
        sim.executable = 'pmemd.cuda'
        sim.prefix = 'prod.'+curr
        sim.input = 'mdin'
        sim.inpcrd = os.path.join(oworkdir, 'equil.rst7')
        sim.ref = os.path.join(oworkdir, 'solvated.rst7')
        sim.cntrl['ntx'] = 5
        sim.cntrl['irest'] = 1
        sim.cntrl['nstlim'] = itr_nstlim
        sim.cntrl['ntwr'] = itr_nstlim
        sim.cntrl['ntwx'] = 250
        sim.cntrl['ntwprt'] = 196
        sim.cntrl['ntxo'] = 2
        sim.cntrl['cut'] = 9.0
        output_filename = str(sim.output)
        sim.output = os.path.join(oworkdir, output_filename)
        if not sim.has_timings():
            sim.output = output_filename
            sim.run()
            sp.call(['rsync','-au', tmpdir+'/', oworkdir+'/'])
    else:
        sim.prefix = 'prod.'+curr
        sim.inpcrd = os.path.join(oworkdir, 'prod.'+prev+'.rst7')
        sim.ref = os.path.join(oworkdir,'solvated.rst7')
        sim.input = 'mdin'
        output_filename = str(sim.output)
        sim.output = os.path.join(oworkdir, output_filename)
        if not sim.has_timings():
            sim.output = output_filename
            sim.run()
            sp.call(['rsync','-au', tmpdir+'/', oworkdir+'/'])
   
