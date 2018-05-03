import os as os
import shutil as shutil
import re as re

import paprika as paprika
from paprika.amber import Simulation

import logging

logging.basicConfig(
    filename='tscc.log',
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=logging.DEBUG)
logging.info('Started logging...')
logging.info(paprika.__version__)

ntwprt = 206
nstlim = 500000

sim = Simulation()

# Minimization
sim.executable = 'pmemd.cuda'
sim.topology = 'solvate.prmtop'
sim.prefix = 'minimize'
sim.inpcrd = 'solvate.rst7'
sim.path = './'
sim.ref = 'solvate.rst7'
sim.config_pbc_min()
sim.cntrl['maxcyc'] = 500
sim.cntrl['ncyc'] = 400
sim.cntrl['ntr'] = 1
sim.cntrl['restraint_wt'] = 50.0
sim.cntrl['restraintmask'] = "'@DUM'"
sim.cntrl['cut'] = 9.0
sim.restraint_file = 'disang.rest'
sim.run(fail_ok=False)

# Equilibration
sim.config_pbc_md()
sim.executable = 'pmemd.cuda'
sim.topology = 'solvate.prmtop'
sim.path = './'
sim.restraint_file = 'disang.rest'

sim.cntrl['nstlim'] = nstlim
sim.cntrl['ntwx'] = 250
sim.cntrl['ntwprt'] = ntwprt
sim.cntrl['ntwr'] = 250
sim.cntrl['cut'] = 9.0

iteration = 0
sim.prefix = 'equil.{:03d}'.format(iteration)
sim.inpcrd = 'minimize.rst7'
sim.ref = 'solvate.rst7'

while not os.path.isfile('equil.rst7') and iteration < 10:
    sim.run(fail_ok=True)
    with open('equil.{:03d}.out'.format(iteration)) as f:
        for line in f.readlines():
            if re.search(' TIMINGS', line):
                shutil.copy(sim.restart, 'equil.rst7')
    iteration += 1
    sim.prefix = 'equil.{:03d}'.format(iteration)
    sim.inpcrd = 'equil.{:03d}.rst7'.format(iteration - 1)
    sim.ref = 'solvate.rst7'

# Production
for iteration in range(0, 5):
    sim.executable = 'pmemd.cuda'
    sim.path = './'
    sim.topology = 'solvate.prmtop'
    sim.restraint_file = 'disang.rest'
    sim.config_pbc_md()

    sim.prefix = 'prod.{:03d}'.format(iteration)
    if iteration == 0:
        sim.inpcrd = 'equil.rst7'
    else:
        sim.inpcrd = 'prod.{:03d}.rst7'.format(iteration - 1)

    sim.ref = 'solvate.rst7'
    sim.cntrl['ntx'] = 5
    sim.cntrl['irest'] = 1
    sim.cntrl['nstlim'] = nstlim
    sim.cntrl['ntwr'] = nstlim
    sim.cntrl['ntwx'] = 250
    sim.cntrl['ntwprt'] = ntwprt
    sim.cntrl['ntxo'] = 2
    sim.cntrl['cut'] = 9.0
    sim.restraint_file = 'disang.rest'
    sim.run(fail_ok=False)
