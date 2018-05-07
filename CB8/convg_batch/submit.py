import numpy as np
import subprocess as sp
import os

for i in range(0,5):
    for frac in np.arange(0.01, 1.01, 0.01):
        with open('ts.sub', 'w') as f:
            f.write("""
#!/bin/bash
#PBS -S /bin/bash
#PBS -l walltime=08:00:00,nodes=1:ppn=4 -q home
#PBS -j oe -r n -m n -M shireham@gmail.com
#PBS -N TS-conf{0}_{1:.2f}

source /home/henrikse/paprika_install/env.sh

cd $PBS_O_WORKDIR
python convergence.py {0} {1:.2f}
""".format(i,frac))
        if not os.path.isfile('CB8-G3-{0}-ti-block-{1:.2f}.dat'.format(i,frac)):
            print('Submitting {0} {1:.2f}'.format(i,frac))
            #sp.call(['qsub','ts.sub'])

