import time
import os

from smac import HyperparameterOptimizationFacade, Scenario
from ConfigSpace import Configuration, ConfigurationSpace
import subprocess




def train(config: Configuration, seed: int = 0): #-> float:
    totaltime = 0
    for file in os.listdir("../instances/train/coloring/"):
        if file.endswith(".cnf"):
            args = ("../kissat/kissat", 
                "../instances/train/coloring/" + file, 
                "--target=" + str(config["target"]),
                "--restartint=" + str(config["restartint"]),
                "--probeint=" + str(config["probeint"]),
                "--vivify=" +str(config["vivify"]),
                "--ands=" + str(config["ands"]),
                "--time=1000",
                "-n",
		        "-q")
            start = time.time()
            popen = subprocess.Popen(args)
            popen.wait()
            end = time.time()
            totaltime += end - start
    return totaltime





configspace = ConfigurationSpace({"target": (0, 2), "restartint": (1,10000), "probeint": (2, 1000), "vivify": ["true", "false"], "ands": ["true","false"]})

# Scenario object specifying the optimization environment
scenario = Scenario(configspace, deterministic=True, n_trials=60, objectives="runtime")

# Use SMAC to find the best configuration/hyperparameters
smac = HyperparameterOptimizationFacade(scenario, train)
incumbent = smac.optimize()
print(incumbent)
