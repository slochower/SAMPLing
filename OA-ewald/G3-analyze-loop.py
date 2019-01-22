import glob as glob
import subprocess as sp
import os as os

g3_complexes = sorted(glob.glob('OA-G3-*'))
g3_complexes = [i for i in g3_complexes if os.path.isdir(i)]
for complx in g3_complexes:

    print('Running python G3-analyze.py --name {}'.format(complx))
    sp.Popen(['python G3-analyze.py --name {}'.format(complx)], shell=True)
