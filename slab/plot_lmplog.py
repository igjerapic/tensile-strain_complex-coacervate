import sys

import matplotlib.pyplot as plt 
import pandas as pd 

from utils.lmptools import readlmplog




def main(args):
    log = readlmplog(args[0])
    keywords = log[0]["keywords"]
    df = pd.DataFrame(data=log[-3]["data"], columns=log[-3]["keywords"])

    if len(args) == 1: 
        print(keywords)
        print(f"num runs {len(log)}")
        return -1

    ylabel = args[1]
    xlabel = "Time"

    df.plot(x=xlabel, y=ylabel, xlabel="Time", ylabel=ylabel)
    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    main(sys.argv[1:])

