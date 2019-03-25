import sys

import random
import math
from cpu import cpuFCFS, cpuSJF, cpuSRT, cpuRR
from process import process
import copy

####
###  Argumnets <random number generator seed> <arrival time lambda> <random number max> <num processes> <context switch time> <exponential averaging alpha> <time slice> <RR BEGINNING/END>
##

## Taken from https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
## as suggested on piazza (@247)
class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def drand(self):
        return self.next() / 2**48

def run(cpu, processes, maxATime):
	for process in sorted(processes, key=lambda x: x.arrivalTime):
		print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.uID, process.arrivalTime, len(process.cpuBursts)))

	time = 0
	print("time 0ms: Simulator started for {} {}".format(cpu.cpuType, str(cpu)))
	while not cpu.isDone() or time <= maxATime:
		for process in processes:
			if process.arrivalTime == time:
				cpu.add(process)
				print("time {}ms: Process {} arrived; added to ready queue {}".format(time, process.uID, str(cpu)))
		cpu.update(time)
		time += 1
	print("time {}ms: Simulator ended for {} {}".format(time, cpu.cpuType, str(cpu)))

if __name__ == "__main__":
	r = Rand48(0)
	seed = int(sys.argv[1])
	rand = Rand48(0)
	rand.srand(seed)
	lambdaa = float(sys.argv[2])
	randMax = int(sys.argv[3])
	numProcesses = int(sys.argv[4])
	contextSwitch = int(sys.argv[5])
	alpha = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
	rr = sys.argv[7] if len(sys.argv) > 7 else "END"

	processes = []
	maxATime = 0
	for i in range(numProcesses):
		## Exponential random for arrival time
		x = -1
		while x > randMax or x == -1:
			x = -math.log(rand.drand())/lambdaa
		aTime = math.floor(x)
		## Variables for cpu bursts
		numBursts = math.floor(rand.drand() * 100) + 1
		cpuBursts = []
		ioBursts = []
		for j in range(numBursts):
			## Exponential random for cpu burst
			x = -1
			while x > randMax or x == -1:
				x = -math.log(rand.drand())/lambdaa
			cpuBursts.append(math.ceil(x))
			## One less I/O burst than cpu burst
			if j < numBursts -1:
				## Exponential random for I/O burst
				x = -1
				while x > randMax or x == -1:
					x = -math.log(rand.drand())/lambdaa
				ioBursts.append(math.ceil(x))
		maxATime = max(maxATime, aTime)
		processes.append(process(chr(ord("A") + i), cpuBursts, ioBursts, aTime))

	f= open("simout.txt","w+")

	####
	### SJF
	##

	cpu = cpuSJF(contextSwitch)
	run(cpu, copy.deepcopy(processes), maxATime)
	print()

	# avgBurst = 0
	avgBurst = sum(cpu.bursts)/len(cpu.bursts)

	f.write("Algorithm SJF\n")
	f.write("-- average CPU burst time: {0:.3f} ms\n".format(avgBurst))
	f.write("-- average wait time: 0.000 ms\n")	# Actually record wait time
	f.write("-- average turnaround time: {0:.3f} ms\n".format(avgBurst + contextSwitch))
	f.write("-- total number of context switches: {}\n".format(cpu.switches))
	f.write("-- total number of preemptions: 0\n")

	####
	### SRT
	##

	cpu = cpuSRT(contextSwitch)
	run(cpu, copy.deepcopy(processes), maxATime)
	print()

	# avgBurst = 0
	avgBurst = sum(cpu.bursts)/len(cpu.bursts)

	f.write("Algorithm SRT\n")
	f.write("-- average CPU burst time: {0:.3f} ms\n".format(avgBurst))
	f.write("-- average wait time: 0.000 ms\n")	# Actually record wait time
	f.write("-- average turnaround time: {0:.3f} ms\n".format(avgBurst + contextSwitch))
	f.write("-- total number of context switches: {}\n".format(cpu.switches))
	f.write("-- total number of preemptions: 0\n")

	####
	### FCFS
	##

	cpu = cpuFCFS(contextSwitch)
	run(cpu, copy.deepcopy(processes), maxATime)
	print()

	avgBurst = sum(cpu.bursts)/len(cpu.bursts)

	f.write("Algorithm FCFS\n")
	f.write("-- average CPU burst time: {0:.3f} ms\n".format(avgBurst))
	f.write("-- average wait time: 0.000 ms\n")	# Actually record wait time
	f.write("-- average turnaround time: {0:.3f} ms\n".format(avgBurst + contextSwitch))
	f.write("-- total number of context switches: {}\n".format(cpu.switches))
	f.write("-- total number of preemptions: 0\n")

	####
	### RR
	##

	cpu = cpuRR(contextSwitch, int(sys.argv[7]), sys.argv[8] if len(sys.argv) == 9 else "END")
	run(cpu, copy.deepcopy(processes), maxATime)

	# avgBurst = 0
	avgBurst = sum(cpu.bursts)/len(cpu.bursts)

	f.write("Algorithm RR\n")
	f.write("-- average CPU burst time: {0:.3f} ms\n".format(avgBurst))
	f.write("-- average wait time: 0.000 ms\n")	# Actually record wait time
	f.write("-- average turnaround time: {0:.3f} ms\n".format(avgBurst + contextSwitch))
	f.write("-- total number of context switches: {}\n".format(cpu.switches))
	f.write("-- total number of preemptions: 0\n")

	f.close()