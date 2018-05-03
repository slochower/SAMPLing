import glob as glob
import subprocess as sp
import os as os

directories = glob.glob('OA-G*/AMBER/APR/windows/*')

for directory in directories:
     if not os.path.isfile(os.path.join(directory, 'prod.004.nc')):
        print(f'Running qsub tscc-driver.sh in {directory}')
        sp.call("qsub tscc-driver.sh", cwd=directory, shell=True)
