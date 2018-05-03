import glob as glob
import os as os
import numpy as np
import sys as sys

all_complexes = sorted(glob.glob('OA-G*'))

for complex_index, complx in enumerate(sorted(all_complexes)):
    windows = sorted(glob.glob(os.path.join(complx, 'AMBER', 'APR', 'windows', '*')))
    for window in windows:
        if not os.path.isfile(os.path.join(window, 'prod.004.nc')):
            print(window)
