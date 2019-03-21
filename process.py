class process:
	def __init__(self, uID, cpuBursts, ioBursts, aTime):
		self.state = "ready"
		self.uID = uID
		self.cpuBursts = cpuBursts
		self.ioBursts = ioBursts
		self.timeRemaining = sum(cpuBursts) + sum(ioBursts)
		self.arrivalTime = aTime
		self.timeFinished = -9999

	def timeRan(self, time, realTime):
		self.timeRemaining-=time
		if (timeRemaining == 0):
			self.state="finished"
			self.timeFinished = realTime
