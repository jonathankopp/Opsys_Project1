import sys

import random
import math
from cpu import cpuFCFS, cpuSJF
from process import process
import copy

####
###  Argumnets <random number generator seed> <arrival time lambda> <random number max> <num processes> <context switch time> <exponential averaging alpha> <time slice> <RR BEGINNING/END>
##

class rand:
	def __init__(self, seed):
		self.seed = seed
		self.a = 0x5DEECE66D
		self.c = 0xB

	def drand(self):
		self.seed = (self.a * self.seed + self.c) % 2**48
		return self.seed / 2**48

def run(cpu, processes, maxATime):
	time = 0
	while not cpu.isDone() or time <= maxATime:
		cpu.update(time)
		for process in processes:
			if process.arrivalTime == time:
				cpu.add(process)
		time += 1

if __name__ == "__main__":
	seed = int(sys.argv[1])
	rand = rand(seed)
	lambdaa = float(sys.argv[2])
	randMax = int(sys.argv[3])
	numProcesses = int(sys.argv[4])
	contextSwitch = int(sys.argv[5])
	alpha = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
	rr = sys.argv[7] if len(sys.argv) > 7 else "END"

	processes = []
	maxATime = 0
	for i in range(numProcesses):
		r = rand.drand()
		x = -math.log(r)
		if x > randMax:
			i -= 1
			continue
		numBursts = math.floor(r * 100) + 1
		cpuBursts = []
		ioBursts = []
		for j in range(numBursts):
			burst = math.ceil(-math.log(random.uniform(0, 1)))
			cpuBursts.append(burst)
			if j < numBursts -1:
				burst = math.ceil(-math.log(random.uniform(0, 1)))
				ioBursts.append(burst)
		aTime = math.floor(x)
		maxATime = max(maxATime, aTime)
		processes.append(process("A"+str(i), cpuBursts, ioBursts, aTime))

	print("Context switch time: " + str(contextSwitch) + "ms")

	cpu = cpuFCFS(contextSwitch)
	run(cpu, copy.deepcopy(processes), maxATime)

	# cpu = cpuSJF(contextSwitch)
	# run(cpu, copy.deepcopy(processes), maxATime)