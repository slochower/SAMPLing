import os as os
import glob as glob
import subprocess as sp

complexes = sorted(glob.glob('CB8-G3*'))
complexes = [i for i in complexes if os.path.isdir(i)]

for complx in complexes:
    with open(complx + '-wall-time.log', 'w') as f:
        f.write(f'Complex Seconds\n')
        directories = glob.glob(os.path.join(complx, 'windows/') + 'a0*') + \
                    glob.glob(os.path.join(complx, 'windows/') + 'p0*')
        trajectories = ['prod.*.out' ]
        # This could also be ``'prod*.out'`, but I have extra sampling in some windows,
        # that I didn't use for the analysis and I want to exclude for the wall-time calculation.
        complx_time = 0
        for directory in directories:
            files = glob.glob(os.path.join(directory, trajectories[0]))
            for file in files:
                command = "grep 'Total wall time:' {}".format(file)
                time = sp.check_output(command, shell=True)
                wall_time = time.decode('utf-8').split()[4]
                #print(f'{file} {wall_time}')
                complx_time += int(wall_time)
        print(f'{complx} {complx_time} seconds')
        f.write(f'{complx} {complx_time}')

