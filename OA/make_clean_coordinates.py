import os
import glob as glob
import parmed as pmd

directories = glob.glob("OA-G*/AMBER/APR/windows/a000")

for directory in directories:
    structure = pmd.load_file(
        os.path.join(directory, "solvate.prmtop"),
        os.path.join(directory, "solvate.rst7"),
    )
    tmp = structure["!@DUM"]
    if os.path.exists(os.path.join(directory, "solvate-no-dummy.prmtop")):
        os.remove(os.path.join(directory, "solvate-no-dummy.prmtop"))
    if os.path.exists(os.path.join(directory, "solvate-no-dummy.rst7")):
        os.remove(os.path.join(directory, "solvate-no-dummy.rst7"))
    tmp.save(os.path.join(directory, "solvate-no-dummy.prmtop"))
    tmp.save(os.path.join(directory, "solvate-no-dummy.rst7"))

