class process:
	def __init__(self, uID, numBursts, burstTime, aTime):
		self.state = "ready"
		self.uID = uID
		self.numBursts = numBursts
		self.burstTime = burstTime
		self.timeRemaining = burstTime
		self.arrivalTime = aTime

