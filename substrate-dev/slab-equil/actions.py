""" Actions for the densities workspace"""

import argparse
import os
import subprocess

import signac

def pack(*jobs):
    for job in jobs:
        sp = job.sp
        lmp_vars = " ".join(f"-v {key} {val}" for key, val in sp.items())

        inscript = project.path + "/lmp_scripts/in.pack" 
        topofile = project.path + "/topologies/linear.mol"
        cmd = f"lmp -i {inscript} -v TOPO_FILE {topofile} {lmp_vars}"
        subprocess.run(cmd, shell=True, check = True)

def slabEquil(*jobs):
    for job in jobs:
        sp = job.sp
        lmp_vars = " ".join(f"-v {key} {val}" for key, val in sp.items())
        name="slabEquil"
        outPattern = job.path + '/' + name 
        # check if process finished
        if job.isfile(outPattern + ".done") : 
            print(outPattern + ".done")
            print("Job is finished")
            continue 

        if job.fn(outPattern + ".outlmp"): 
            outPattern += "_restart"

        inscript = project.path + f"/lmp_scripts/in.{name}" 
        settingsfile = project.path + "/lmp_scripts/settings.lmp" 
        # cmd = f"lmp -i {inscript} -sc {outPattern}.outlmp -l {outPattern}.loglmp {lmp_vars}"
        cmd = f"lmp -i {inscript}  -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} {lmp_vars}"
        subprocess.run(cmd, shell=True, check = True)

if __name__ == '__main__':
    # Parse the command line arguments: python action.py --action <ACTION> [DIRECTORIES]
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True)
    parser.add_argument('directories', nargs='+')
    args = parser.parse_args()

    # Open the signac jobs
    project = signac.get_project()
    jobs = [project.open_job(id=directory) for directory in args.directories]

    # Call the action
    globals()[args.action](*jobs)

