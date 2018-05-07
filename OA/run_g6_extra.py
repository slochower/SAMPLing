import glob as glob
import subprocess as sp

directories = glob.glob('OA-G6*/AMBER/APR/windows/*')

for directory in directories:
    print(f'Running qsub tscc-driver.sh in {directory}')
    sp.call("qsub tscc-driver.sh", cwd=directory, shell=True)
