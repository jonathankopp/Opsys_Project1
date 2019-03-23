class process:
	def __init__(self, uID, cpuBursts, ioBursts, aTime):
		self.state = "ready"
		self.uID = uID
		self.cpuBursts = cpuBursts
		self.ioBursts = ioBursts
		self.arrivalTime = aTime
		self.timeFinished = -9999

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