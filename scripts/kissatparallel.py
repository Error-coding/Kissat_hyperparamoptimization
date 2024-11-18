import time
import sys
import random

from smac import HyperparameterOptimizationFacade, Scenario
from ConfigSpace import Configuration, ConfigurationSpace, EqualsCondition, Categorical, Integer
import subprocess

from gbd_core.api import GBD
    


instancegroup = int(sys.argv[1]) #index of the instance family group to get from gbd (family groups are defined in instance_families.txt)

timeout = int(sys.argv[2]) #timeout for a single instance

kinstances = int(sys.argv[3]) #take k instances out of training set each run


def printenv(output):
    print("Task " + str(instancegroup) + ":" + output)

def getinstances(instancegroup):
    f=open("../instances_families.txt")
    lines=f.readlines()
    fams = lines[instancegroup].split()[1].split(",")

    famstring = "(family=" + fams[0]

    for i in range(1, len(fams)):
        famstring += " or family=" + fams [i]
    famstring += ")"

    with GBD (["/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/meta.db" , "/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/instances.db"]) as gbd:
        
        feat = ["instances:local"]
        df = gbd.query ( "(track=main_2023 or track=main_2024) and family=coloring and minisat1m!=yes", resolve = feat)
        return df["local"].tolist()


def train(config: Configuration, seed: int = 0): #-> float:
    totaltime = 0
    for file in random.shuffle(getinstances(instancegroup))[:kinstances]:
        printenv()
        args = ("../kissat/kissat", 
            file, 
            "--time=" + str(timeout),
            "-q",
            "-n")

        for key in config:
            arg = "--" + key + "=" + str(config[key])
            args = args + (arg,)

        start = time.time()
        try:
            output = subprocess.run(args, capture_output=True)
        except:
            printenv("Solver failed")
            
        end = time.time()
        outputstr = output.stdout.decode()

        status = False
        for line in outputstr.splitlines():
            line = line.strip()
            if (line == r's SATISFIABLE') or (line == r's UNSATISFIABLE'):
                printenv("Solved")
                status = True
                break
            elif line == r's UNKNOWN':
                printenv("Timeout")
                status = False
                break

        if(status):
            totaltime += end - start
        else:
            totaltime += 2 * timeout
    return totaltime



random.seed(31)

configspace = ConfigurationSpace({"phase": (0, 2), "target": (0, 2), 
                                "restartint": (1,10000), 
                                "probeint": (2, 1000), 
                                "backbone": (0, 2),
                                "vivifyirr": (0,100),
                                "sweepclauses": (0, 2147483647)
                                })


congruenceands = Categorical("congruenceands", items=["true", "false"])
congruenceandarity = Integer("congruenceandarity", bounds=(1, 50000000), log=True, default=1000000)

congruencexors = Categorical("congruencexors", items=["true", "false"])
congruencexorarity = Integer("congruencexorarity", bounds=(2, 20))

configspace.add([congruenceands, congruenceandarity])
configspace.add([congruencexors, congruencexorarity])


configspace.add(EqualsCondition(congruenceandarity, congruenceands, "true"))
configspace.add(EqualsCondition(congruencexorarity, congruencexors, "true"))

# Scenario object specifying the optimization environment
scenario = Scenario(configspace, deterministic=True, n_trials=10, objectives="runtime", output_directory = "../outputs/" + str(instancegroup))

# Use SMAC to find the best configuration/hyperparameters
smac = HyperparameterOptimizationFacade(scenario, train)
incumbent = smac.optimize()
printenv(incumbent)