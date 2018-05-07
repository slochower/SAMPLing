import glob as glob
import os as os
import numpy as np
import sys as sys

all_complexes = sorted(glob.glob('OA-G6*'))

for complex_index, complx in enumerate(sorted(all_complexes)):
    windows = sorted(glob.glob(os.path.join(complx, 'AMBER', 'APR', 'windows', '*')))
    counter = 0
    for window in windows:
        if os.path.isfile(os.path.join(window, 'prod.009.nc')):
            counter += 1
    print(f'{complx} {counter}')
