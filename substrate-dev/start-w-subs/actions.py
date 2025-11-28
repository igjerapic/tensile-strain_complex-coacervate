""" Actions for the confined polymer equilibration test """

import argparse
import os
import subprocess

import signac

def pack(*jobs):
    for job in jobs:
        action = "pack"
        # skip if action is already completed
        if job.isfile(f"{action}.done") : continue

        outPattern = job.path + '/' + action
        inscript = project.path + f"/lmp_scripts/in.{action}" 
        topofile = project.path + "/topologies/linear.mol"
        lmp_vars = " ".join(f"-v {key} {val}" for key, val in job.sp.items())
        cmd = f"lmp -i {inscript} -v TOPO_FILE {topofile} -v JOBDIR {job.path} -v ACTION {action} {lmp_vars}"
        subprocess.run(cmd, shell=True, check = True)

def equil(*jobs):
    for job in jobs:
        action="equil"
        # skip if action is already completed
        if job.isfile(f"{action}.done") : continue

        # output files w.r.t project directory
        outPattern = job.path + '/' + action 
        if job.isfile(f"{action}.outlmp"):
            outPattern += "_restart"

        # create LAMMPS command
        inscript = project.path + f"/lmp_scripts/in.{action}" 
        settingsfile = project.path + "/lmp_scripts/settings.lmp" 
        lmp_vars = " ".join(f"-v {key} {val}" for key, val in job.sp.items())
        cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"
        # cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"

        # run LAMMPS command
        subprocess.run(cmd, shell=True, check = True)

# def equil_restart(*jobs):
#     for job in jobs:
#         action="equil_restart"
#         # skip if action is already completed
#         if job.isfile(f"{action}.done") : continue
# 
#         # output files w.r.t project directory
#         outPattern = job.path + '/' + action 
#         # if job.isfile(f"{action}.outlmp"): 
#         #     outPattern += "_restart"
# 
#         # create LAMMPS command
#         inscript = project.path + f"/lmp_scripts/in.{action}" 
#         settingsfile = project.path + "/lmp_scripts/settings.lmp" 
#         lmp_vars = " ".join(f"-v {key} {val}" for key, val in job.sp.items())
#         cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"
#         # cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"
# 
#         # run LAMMPS command
#         subprocess.run(cmd, shell=True, check = True)
# def slabEquil(*jobs):
#     for job in jobs:
#         action="slabEquil"
#         # skip if action is already completed
#         if job.isfile(f"{action}.done") : continue
#
#         # output files w.r.t project directory
#         outPattern = job.path + '/' + action 
#         if job.isfile(f"{action}.outlmp"): 
#             outPattern += "_restart"
#
#         # create LAMMPS command
#         inscript = project.path + f"/lmp_scripts/in.{action}" 
#         settingsfile = project.path + "/lmp_scripts/settings.lmp" 
#         lmp_vars = " ".join(f"-v {key} {val}" for key, val in job.sp.items())
#         cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"
#
#         # run LAMMPS command
#         subprocess.run(cmd, shell=True, check = True)
#
# def subEquil(*jobs):
#     for job in jobs:
#         action="subEquil"
#         # skip if action is already completed
#         if job.isfile(f"{action}.done") : continue
#
#         # output files w.r.t project directory
#         outPattern = job.path + '/' + action
#         if job.isfile(f"{action}.outlmp"): 
#             outPattern += "_restart"
#
#         # create LAMMPS command
#         inscript = project.path + f"/lmp_scripts/in.{action}" 
#         settingsfile = project.path + "/lmp_scripts/settings.lmp" 
#         lmp_vars = " ".join(f"-v {key} {val}" for key, val in job.sp.items())
#         cmd = f"lmp -sf omp -pk omp $ACTION_THREADS_PER_PROCESS -i {inscript} -sc {outPattern}.outlmp -l {outPattern}.loglmp -v JOBDIR {job.path} -v SETTINGS_FILE {settingsfile} -v ACTION {action} {lmp_vars}"
#
#         # run LAMMPS command
#         subprocess.run(cmd, shell=True, check = True)

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

