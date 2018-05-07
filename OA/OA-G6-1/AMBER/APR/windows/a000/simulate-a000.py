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

# Production
for iteration in range(0, 20):
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
    sim.restraint_file = 'disang.rest'
    sim.run(fail_ok=False)
