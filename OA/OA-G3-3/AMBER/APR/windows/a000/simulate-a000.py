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

dummy_anchors = [':3', ':4', ':5']
host_anchors = [':1@C26', ':1@C18', ':1@C8']
guest_anchors = [':2@C1', ':2@C3']

ntwprt = 204
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
