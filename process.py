import math

class process:
	def __init__(self, uID, cpuBursts, ioBursts, aTime, tau):
		self.state = "ready"
		self.uID = uID
		self.cpuBursts = cpuBursts
		self.ioBursts = ioBursts
		self.arrivalTime = aTime
		self.timeFinished = -9999
		self.tau = tau
		self.lastBurst = 0

	def recalculateTau(self, alpha):
		self.tau = math.floor((alpha * self.lastBurst) + ((1-alpha) * self.tau))

	def isDone(self, time):
		if(len(self.ioBursts) == 0 and len(self.cpuBursts) == 0):
			# print("["+self.uID+" is done at "+str(time)+"]")
			return True
		return False

	def ioBurstFinished(self):
		if(len(self.ioBursts) == 1):
			self.ioBursts = []
			return
		self.ioBursts = self.ioBursts[1:]

	def cpuBurstFinished(self):
		if(len(self.cpuBursts) == 1):
			self.cpuBursts = []
			return
		self.cpuBursts = self.cpuBursts[1:]
		self.lastBurst = self.cpuBursts[0]