import sys
import argparse
import pickle as pkl
import re
import yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader

import matplotlib.pyplot as plt 
import pandas as pd 
import signac


def readlog(action, update, job):
    file = f"{job.path}/{action}.loglmp"
    if (not update) and (job.isfile(f"{action}_log.pkl")):
        thermo = pkl.load(open(f"{job.path}/{action}_log.pkl", 'rb'))
        return thermo

    docs = ""
    with open(file) as f:
        for line in f:
            m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
            if m: docs += m.group(0) + '\n'

    thermo = list(yaml.load_all(docs, Loader=Loader))

    pkl.dump(thermo, open(f"{job.path}/{action}_log.pkl", 'wb'))
    return thermo

def convertToPandas(thermo, runIdx=None):
    simLength = len(thermo)
    if not (runIdx is None) or (simLength==1): 
        if (runIdx is None) and (simLength==1): runIdx = 0
        return pd.DataFrame(data=thermo[runIdx]['data'], columns=thermo[runIdx]['keywords']), simLength
    data = {}
    keywords = thermo[0]["keywords"]
    for key in keywords:
        for run in range(simLength):
            df = pd.DataFrame(data=thermo[run]["data"], columns=thermo[run]["keywords"]) 
            
            # Keep data values, but adjust time to show total simulatino time in tau
            if key != "Time": 
                data.setdefault(key, []).append(df[key].to_numpy())
                continue
            runtime = df[key].to_numpy()
            if run == 0:
                data[key] = [runtime]
                print(run, data[key][run][-1])
                continue
            tmptime = runtime  - runtime[0] + data[key][run - 1][-1]
            data[key].append(tmptime)
    return data, simLength

def plot(action, data, simLength, job, y=None, x="Time", runIdx = None, saveFig = False, show = False):
    sp = job.sp
    run_label = "Total" if runIdx is None else runIdx
    charge_label = "charged" if sp.isCharged == "True" else "neutral" 
    title = f"{sp.wallPot}_epLJ{sp.epLJ}_sigma{sp.subSigma}_{charge_label}_{run_label}"
    interval = 2500
    start_step = int(2e5)
    startIdx = start_step/interval
    startIdx = 0
    if not (y is None):
        if (runIdx is None) and (simLength != 1):
            print(data)
            for run in range(simLength):
                plt.plot(data[x][run][startIdx:], data[y][run][startIdx:]) 
        else:
            data = data.loc[startIdx:]
            data.plot(x=x, y=y)
        plt.title(title, fontsize=12)
        plt.ylabel(y)
        plt.tight_layout()
        if saveFig:
            file_name = f"{job.path}/figs/{action}_{y}_{x}.png"
            plt.savefig(file_name, dpi=300, format="png")
        if show: plt.show()
        return 0

    for key in data.keys():
        if key == x: continue
        plt.clf()

        if runIdx is None:
            for run in range(len(data[key])):
                plt.plot(data[x][run], data[key][run]) #, color=f"C{run+3}")#, label = run_label[run])
        else:
            data.plot(x=x, y=key)
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(key)
        plt.tight_layout()
        if saveFig:
            file_name = f"{job.path}/figs/{action}_{key}_{x}.png"
            plt.savefig(file_name, dpi=300, format="png")
        if show: plt.show()
    return 0

def run_plotter(action, x, y, update, runIdx, save, show, job):
    thermo = readlog(action, update, job)
    data, simLength = convertToPandas(thermo, runIdx)
    plot(action, data, simLength, job, y=y, x=x, runIdx = runIdx, saveFig = save, show = show)

if __name__ == '__main__':
    # Parse the command line arguments: python action.py --action <ACTION> [DIRECTORIES]
    parser = argparse.ArgumentParser()
    parser.add_argument('logfile',  type=str)
    parser.add_argument('-x', '--x_axis', default="Step")
    parser.add_argument('-y', '--y_axis', nargs='+', default=None)
    parser.add_argument('-u', '--update', default=False, type = bool, help='rereads and updates the pkl file of the lof file (default : %(default)s)')
    parser.add_argument('-r', '--runIdx',  default=None, type=int, help='the run index of the simulation using python list numbering, providing nothing will go through all runs')
    parser.add_argument('-s', '--save', nargs=1, default=False, type=bool, help="saves the resulting plot in a png (default: %(default))")
    parser.add_argument('--show',  default=True, type=bool, help="shows the reslting plot (default: %(default))")
    parser.add_argument('directories', nargs='+')
    args = parser.parse_args()
    print(args)

    # Open the signac jobs
    project = signac.get_project()
    jobs = [project.open_job(id=directory) for directory in args.directories]

    # Call the action
    for job in jobs:
        run_plotter(action = args.logfile, x=args.x_axis, y=args.y_axis, update=args.update, runIdx=args.runIdx, save=args.save, show=args.show, job = job)

