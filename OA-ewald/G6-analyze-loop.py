import glob as glob
import subprocess as sp
import os as os

g6_complexes = sorted(glob.glob('OA-G6-*'))
g6_complexes = [i for i in g6_complexes if os.path.isdir(i)]
for complx in g6_complexes:

    print('Running python G6-analyze.py --name {}'.format(complx))
    sp.Popen(['python G6-analyze.py --name {}'.format(complx)], shell=True)
