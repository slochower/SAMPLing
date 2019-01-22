import os as os
import glob as glob

directories = glob.glob('OA-G3-*/AMBER/APR/windows/*')

for directory in directories:
    try:
        os.symlink('../../../../../G3_simulate.py', os.path.join(directory, 'simulate.py'))
    except:
        os.remove(os.path.join(directory, 'simulate.py'))
        os.symlink('../../../../../G3_simulate.py', os.path.join(directory, 'simulate.py'))

    try:
        os.symlink('../../../../../tscc-driver.sh',
                   os.path.join(directory, 'tscc-driver.sh'))
    except:
        os.remove(os.path.join(directory, 'tscc-driver.sh'))
        os.symlink('../../../../../tscc-driver.sh',
                   os.path.join(directory, 'tscc-driver.sh'))

directories = glob.glob('OA-G6-*/AMBER/APR/windows/*')

for directory in directories:
    try:
        os.symlink('../../../../../G6_simulate.py', os.path.join(directory, 'simulate.py'))
    except:
        os.remove(os.path.join(directory, 'simulate.py'))
        os.symlink('../../../../../G6_simulate.py', os.path.join(directory, 'simulate.py'))

    try:
        os.symlink('../../../../../tscc-driver.sh',
                   os.path.join(directory, 'tscc-driver.sh'))
    except:
        os.remove(os.path.join(directory, 'tscc-driver.sh'))
        os.symlink('../../../../../tscc-driver.sh',
                   os.path.join(directory, 'tscc-driver.sh'))
