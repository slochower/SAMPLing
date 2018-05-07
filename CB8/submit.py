import glob as glob
import subprocess as sp
import shutil
import os

#for conf in [0,1,2,3]:
for conf in [4]:
    directories = glob.glob('CB8-G3-{}/windows/*'.format(conf))
    
    for directory in directories:
        with open(directory+'/ts.sub', 'w') as f:
            f.write("""
    #!/bin/bash
    #PBS -S /bin/bash
    #BS -l walltime=96:00:00,nodes=1:ppn=2:gpu -q home-gibbs -A mgilson-gibbs
    #PBS -l walltime=96:00:00,nodes=1:ppn=3:gpu -q home
    #BS -l walltime=08:00:00,nodes=1:ppn=3:gpu -q glean
    #PBS -j oe -r n -m a -M shireham@gmail.com
    #PBS -N TS-{}
    
    source /home/henrikse/paprika_install/env.sh
    
    cd $TMPDIR
    cp -p $PBS_O_WORKDIR/restraints.in ./
    python $PBS_O_WORKDIR/execute.py
    sleep 2
    rsync -au ./ $PBS_O_WORKDIR/
    """.format(directory))
        shutil.copy('execute.py', directory)
        #if not os.path.isfile( os.path.join(directory, 'minimize.rst7') ):
        #    print('Submitting {}'.format(directory))
        #    sp.call("qsub ts.sub", cwd=directory, shell=True)
        print('Submitting {}'.format(directory))
        sp.call("qsub ts.sub", cwd=directory, shell=True)
