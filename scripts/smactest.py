import time
import os

from smac import HyperparameterOptimizationFacade, Scenario
from ConfigSpace import Configuration, ConfigurationSpace
import subprocess




def train(config: Configuration,instance:str, seed: int = 0): #-> float:
	totaltime = 0
	args = ("../kissat/kissat", 
		instance,
		"--target=" + str(config["target"]),
		"--restartint=" + str(config["restartint"]),
		"--probeint=" + str(config["probeint"]),
		"--time=120",
		"-n",
		"-q")
	start = time.time()
	popen = subprocess.Popen(args)
	popen.wait()
	end = time.time()
	totaltime += end - start
	return totaltime





configspace = ConfigurationSpace({"target": (0, 2), "restartint": (1,10000), "probeint": (2, 1000)})

# Scenario object specifying the optimization environment
scenario = Scenario(configspace, deterministic=True, n_trials=10, objectives="runtime", instances=["../instances/easy/1.cnf", "../instances/easy/2.cnf", "../instances/easy/0.cnf"])

# Use SMAC to find the best configuration/hyperparameters
smac = HyperparameterOptimizationFacade(scenario, train)
incumbent = smac.optimize()
print(incumbent)
