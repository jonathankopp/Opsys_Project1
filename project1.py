import sys

####
###  Argumnets <random number generator seed> <arrival time lambda> <random number max> <num processes> <context switch time> <exponential averaging alpha> <time slice> <RR BEGINNING/END>
##

class rand:
	global seed
	def srand(self, seed):
		self.seed = seed
		self.a = 0x5DEECE66D
        self.c = 0xB
	def drand():
		self.seed = (self.a * self.seed + self.c) % 2^^48
		return self.seed

if __name__ == "__main__":
	seed = int(sys.argv[1])
	lambdaa = float(sys.argv[2])
	randMax = int(sys.argv[3])
	numProcesses = int(sys.argv[4])
	contextSwitch = float(sys.argv[5])
	alpha = float(sys.argv[6]) if sys.argv[6] else 0.0
	rr = sys.argv[7] if sys.argv[7] else "END"
	
	for i in range(numProcesses):
		print()