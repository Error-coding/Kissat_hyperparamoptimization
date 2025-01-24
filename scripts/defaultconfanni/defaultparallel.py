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



#instancegroup = int(sys.argv[1]) #index of the instance family group to get from gbd (family groups are defined in instance_families.txt)

timeout = 1800

#kinstances = int(sys.argv[3]) #take k instances out of training set each run

 #how many times the train function is going to be called

paralleldeg = 32 #how many parallel threads are going to be scheduled

inst = []

def getinstances():
    instlist = []
    with GBD (["/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/meta.db" , "/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/instances.db"]) as gbd:
        
        feat = ["instances:local"]
        df = gbd.query ( "track=anni_2022 and track!=main_2023 and track!=main_2024 and minisat1m!=yes", resolve = feat)
        #print(df["local"].tolist())
        instlist = df["local"].tolist()

    return list(map(lambda x : ("/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/train/" + x.split("/")[-1])[:-3], instlist))

def runKissat(args):
    start = time.time()
    output = None
    try:
    # Run the subprocess without `check=True`
        output = subprocess.run(args, capture_output=True)

    # Check the returncode manually and handle 10 and 20 exit codes
        if output.returncode not in {0, 10, 20}:
            raise subprocess.CalledProcessError(output.returncode, args, output=output.stdout, stderr=output.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error in running kissat: {e}", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
    
    end = time.time()

    if output is None:
        print("No output from kissat, failing after {} seconds".format(end-start), flush=True)
        return 2 * timeout
    
    outputstr = output.stdout.decode()

    status = True
    for line in outputstr.splitlines():
        line = line.strip()
        if (line == r's SATISFIABLE') or (line == r's UNSATISFIABLE'):
            #print(str(instancegroup) + ": Solved", flush=True)
            status = True
            break
        elif line == r's UNKNOWN':
            #print(str(instancegroup) + ": Timeout", flush=True)
            status = False
            break
        else:
            print("Solver failed", flush=True)
            status = False

    if(status):
        print("Instance " + args[1] + "finished after {} seconds".format(end-start), flush=True)
        return end - start
    else:
        print("TIMEOUT: Instance " + args[1] + " has reached timeout, punishment {} seconds".format(2 * timeout), flush=True)
        return 2 * timeout


def train( seed: int = 0): #-> float
    totaltime = 0
    called = 0

    arglist = []
    for file in inst:
        args = ("/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/kissat/kissat_satcomp24", 
                file, 
                "--time=" + str(timeout),
                "-q",
                "-n")
        arglist.append(args)
    
    with pebble.ProcessPool(max_workers=paralleldeg) as p:
        futures = [p.schedule(runKissat, (args,)) for args in arglist]
        for f in as_completed(futures):
            try:    
                totaltime += f.result()
            except Exception as e:
                print(e)
    print(called)
        
    return totaltime

inst = getinstances()

print(len(inst))

print("Terminated after {} seconds".format(train()))