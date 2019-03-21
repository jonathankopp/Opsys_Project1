class process:
	def __init__(self, uID, numBursts, burstTime, aTime):
		self.state = "ready"
		self.uID = uID
		self.numBursts = numBursts
		self.burstTime = burstTime
		self.timeRemaining = burstTime
		self.arrivalTime = aTime
		self.timeFinished = -9999

	def timeRan(self, time, realTime):
		self.timeRemaining-=time
		if (timeRemaining == 0):
			self.state="finished"
			self.timeFinished = realTime
