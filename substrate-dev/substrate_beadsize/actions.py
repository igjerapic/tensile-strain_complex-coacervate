""" Actions for the densities workspace"""

import argparse
import os
import subprocess

import signac

def subEquil(*jobs):
    for job in jobs:
        sp = job.sp
        lmp_vars = " ".join(f"-v {key} {val}" for key, val in sp.items())
        name="subEquil"
        outPattern = job.path + '/' + name

        inscript = project.path + f"/lmp_scripts/in.{name}" 
        settingsfile = project.path + "/lmp_scripts/settings.lmp" 
        cmd = f"lmp -i {inscript} -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} {lmp_vars}"
        # cmd = f"lmp -i {inscript}  -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} {lmp_vars}"
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
