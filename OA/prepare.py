import os as os
import glob as glob

directories = glob.glob('OA-G*/AMBER/APR/windows/a0*') + glob.glob('OA-G*/AMBER/APR/windows/p0*')

for directory in directories:
    files = glob.glob(os.path.join(directory, 'minimize*')) + \
            glob.glob(os.path.join(directory, 'equil*')) + \
            glob.glob(os.path.join(directory, 'prod*'))
    for file in files:
        os.remove(file)
