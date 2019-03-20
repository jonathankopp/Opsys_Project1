import sys
import random
import math
from queueClass import customQueue
from process import process

####
###  Argumnets <random number generator seed> <arrival time lambda> <random number max> <num processes> <context switch time> <exponential averaging alpha> <time slice> <RR BEGINNING/END>
##

# class rand:
# 	def __init__(self, seed):
# 		self.seed = seed
# 		self.a = 0x5DEECE66D
# 		self.c = 0xB

# 	def drand(self):
# 		self.seed = (self.a * self.seed + self.c) % 2**48
# 		return self.seed

if __name__ == "__main__":
	seed = int(sys.argv[1])
	# rand = rand(seed)
	random.seed(seed)
	lambdaa = float(sys.argv[2])
	randMax = int(sys.argv[3])
	numProcesses = int(sys.argv[4])
	contextSwitch = float(sys.argv[5])
	alpha = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
	rr = sys.argv[7] if len(sys.argv) > 7 else "END"

	cpu = customQueue("SRT")

	for i in range(numProcesses):
		# r = rand.drand()
		r = random.uniform(0, 1)
		x = -math.log(r)
		if x > randMax:
			i -= 1
			continue
		cpu.add(process("A", 10, x, 0))