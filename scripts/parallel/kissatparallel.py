import multiprocessing
import time
import sys
import random
import pebble

from smac import HyperparameterOptimizationFacade, Scenario
from ConfigSpace import Configuration, ConfigurationSpace, EqualsCondition, Categorical, Integer
import subprocess

from gbd_core.api import GBD
from concurrent.futures import as_completed
from scripts.confspace.confspace import *



instancegroup = int(sys.argv[1]) #index of the instance family group to get from gbd (family groups are defined in instance_families.txt)

timeout = int(sys.argv[2]) #timeout for a single instance

kinstances = int(sys.argv[3]) #take k instances out of training set each run

ntrials = int(sys.argv[4]) #how many times the train function is going to be called

paralleldeg = int(sys.argv[5]) #how many parallel threads are going to be scheduled

def getinstances():
    print("Getting instances", flush=True)
    f=open("/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances_families.txt")
    lines=f.readlines()
    fams = lines[instancegroup].split()[1].split(",")

    famstring = "(family=" + fams[0]

    for i in range(1, len(fams)):
        famstring += " or family=" + fams [i]
    famstring += ")"


    instlist = []
    with GBD (["/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/meta.db" , "/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/instances.db"]) as gbd:
        
        feat = ["instances:local"]
        df = gbd.query ( "(track=main_2023 or track=main_2024) and " + famstring + " and minisat1m!=yes", resolve = feat)
        print(df["local"].tolist())
        instlist = df["local"].tolist()

    return list(map(lambda x : ("/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/train/" + x.split("/")[-1])[:-3], instlist))

def runKissat(args):
    
        
    start = time.time()
    try:
        output = subprocess.run(args, capture_output=True)
    except:
        print("Solver failed")
            
    end = time.time()
    outputstr = output.stdout.decode()

    status = True
    for line in outputstr.splitlines():
        line = line.strip()
        if (line == r's SATISFIABLE') or (line == r's UNSATISFIABLE'):
            print(str(instancegroup) + ": Solved", flush=True)
            status = True
            break
        elif line == r's UNKNOWN':
            print(str(instancegroup) + ": Timeout", flush=True)
            status = False
            break

    if(status):
        return end - start
    else:
        return 2 * timeout


def train(config: Configuration, seed: int = 0): #-> float:
    totaltime = 0
    


    inst = getinstances()
    arglist = []
    for file in inst[:kinstances]:
        args = ("/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/kissat/kissat", 
                file, 
                "--time=" + str(timeout),
                "-q",
                "-n")

        for key in config:
            arg = "--" + key + "=" + str(config[key])
            args = args + (arg,)
        arglist.append(args)

    with pebble.ProcessPool(max_workers=paralleldeg, context=multiprocessing.get_context('spawn')) as p:
        futures = [p.schedule(runKissat, (args)) for args in arglist]
        for f in as_completed(futures):
            totaltime += f.result

        
    return totaltime

# Scenario object specifying the optimization environment
scenario = Scenario(get_kissat2024_confspace(), deterministic=True, n_trials=ntrials, objectives="runtime", output_directory = "/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/outputs/parallelonefam" + str(instancegroup))

# Use SMAC to find the best configuration/hyperparameters

print("Starting smac")
smac = HyperparameterOptimizationFacade(scenario, train)
incumbent = smac.optimize()
print(incumbent)