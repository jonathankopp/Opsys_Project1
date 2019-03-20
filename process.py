class process:
	def __init__(self, uID, burstTime, aTime):
		self.state = "ready"
		self.uID = uID
		self.burstTime = burstTime
		self.timeRemaining = burstTime
		self.arrivalTime = aTime

