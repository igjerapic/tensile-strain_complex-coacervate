import matplotlib.pyplot as plt 
import pandas as pd 

from utils.lmptools import readlmplog


def main():
    # read log/out file from LAMMPS and get
    file = "totalout.lammps" 
    log = readlmplog(file)
    keywords = log[0]["keywords"]
    run_label = {0: "minimize" , 
                 1: "soft-relax", 
                 2: "sqeeze1"   , 
                 3: "sqeeze2"   , 
                 4: "pressAnn1" , 
                 5: "pressAnn2" , 
                 6: "pressEq"   , 
                 7: "longEq"    , 
                 }

    density = []
    times = []
    totEng = []
    temp = []
    data = {}
    
    for key in keywords:
        for run in range(len(log)):
            df = pd.DataFrame(data=log[run]["data"], columns=log[run]["keywords"]) 
        
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
            print(run, data[key][run][-1])
    
    # plotting
    for key in data.keys():
        if key == 'Time' : continue
        for run in range(len(log)):
            plt.plot(data["Time"][run], data[key][run], label = run_label[run])
        plt.ylabel(key)
        plt.xlabel("Time")
        plt.legend()
        plt.tight_layout()
        plt.show()
    

        # density.append(df["Density"].to_numpy())
        # totEng.append(df["TotEng"].to_numpy())
        # temp.append(df["Temp"].to_numpy())
       
        # offsetting time 
        # runTime = df["Time"].to_numpy()
        # if run == 0:
        #     times.append(runTime)
        #     print(run, times[run][-1])
        #     continue
        # tmptime = runtime  - runtime[0] + times[run - 1][-1]
        # times.append(tmpTime)
        # print(run, times[run][-1])
    
    # plotting
    # for param, label in zip([density, toteng, temp, press], ["density", "toteng", "temp"]):
    #     for run, (time, val) in enumerate(zip(times, param)):
    #         plt.plot(time, val, label = run_label[run] )
    #         plt.xlabel("Time")
    #     plt.ylabel(label)
    #     plt.legend()
    #     plt.show()

if __name__=="__main__":
    main()

