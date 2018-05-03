import os as os
import glob as glob
import subprocess as sp

complexes = sorted(glob.glob('OA-G*'))
complexes = [i for i in complexes if os.path.isdir(i)]

for complx in complexes:
    with open(complx + '-wall-time.log', 'w') as f:
        f.write(f'Complex Seconds\n')
        directories = glob.glob(os.path.join(complx, 'AMBER/APR/windows/') + 'a0*') + \
                    glob.glob(os.path.join(complx, 'AMBER/APR/windows/') + 'p0*')
        trajectories = [
            'prod.000.out', 'prod.001.out', 'prod.002.out', 'prod.003.out',
            'prod.004.out'
        ]
        # This could also be ``'prod*.out'`, but I have extra sampling in some windows,
        # that I didn't use for the analysis and I want to exclude for the wall-time calculation.
        complx_time = 0
        for directory in directories:
            files = [os.path.join(directory, i) for i in trajectories]
            for file in files:
                command = "grep 'Total wall time:' {}".format(file)
                time = sp.check_output(command, shell=True)
                wall_time = time.decode('utf-8').split()[4]
                print(f'{file} {wall_time}')
                complx_time += int(wall_time)
        print(f'{complx} {complx_time} seconds')
        f.write(f'{complx} {complx_time}')
