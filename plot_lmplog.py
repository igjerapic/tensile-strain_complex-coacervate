import sys

import matplotlib.pyplot as plt 
import pandas as pd 

from utils.lmptools import readlmplog


END_PROGRAM = 0

def main(args):
    # read log/out file from LAMMPS and get
    log = readlmplog(args[0])
    keywords = log[0]["keywords"]

    # Show keywords and number of runs as help
    if len(args) == 1: 
        print(keywords)
        print(f"num runs {len(log)}")
        return END_PROGRAM

    # plot chosen attribute as a function of system time
    ylabel = args[1]
    xlabel = "Time"

    df = pd.DataFrame(data=log[-1]["data"], columns=log[-1]["keywords"]) #TODO make which run a choice
    print(ylabel != "all")
    if ylabel != "all":
        df.plot(x=xlabel, y=ylabel, xlabel="Time", ylabel=ylabel)

        plt.tight_layout()
        plt.show()
        return END_PROGRAM

    for key in keywords:
        if key == xlabel : continue
        df.plot(x=xlabel, y=key, xlabel="Time", ylabel=key)
        plt.tight_layout()
        plt.show()

if __name__=="__main__":
    main(sys.argv[1:])

