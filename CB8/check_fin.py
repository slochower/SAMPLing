import glob as glob
import os

directories = glob.glob('CB8-G3-*/windows/*')

for directory in directories:
    file = os.path.join(directory, 'NONE')
    i = 1
    while os.path.isfile( os.path.join(directory, "prod.{:03.0f}.nc".format(i)) ):
        file = os.path.join(directory, "prod.{:03.0f}.nc".format(i))
        i += 1
    #if i-1 < 40:
    #    print(file)
    print(file)
