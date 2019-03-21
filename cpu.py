class cpu:
	def __init__(self, contextSwitch):
		self.queue = []
		self.wait = []
		self.contextSwitch = contextSwitch

	def isDone(self):
		if(len(self.queue) == 0 and len(self.wait) == 0):
			return True
		return False

	# #will return the 0 index (front of the queue) and remove it from the queue
	# def pop(self):
	# 	if(len(self.queue) == 0):
	# 		return None
	# 	Q=[]
	# 	x = 0
	# 	ret = None
	# 	for p in self.queue:
	# 		if(x != 0):
	# 			Q.append(p)
	# 		else:
	# 			ret = p
	# 		x+=1
	# 	self.queue = Q
	# 	return ret


	# #if it is not in the queue it will return false
	# def inQueue(self, process):
	# 	for p in self.queue:
	# 		if(process.uID == p.uID):
	# 			return True
	# 	return False

	# #if id doesnt exsist it will return None	
	# def removeByID(self, uID):
	# 	Q = []
	# 	ret = None
	# 	for p in self.queue:
	# 		if(p.uID != uID):
	# 			Q.append(p)
	# 		else:
	# 			ret = p
	# 	self.queue = Q
	# 	return retdef

	def __str__(self):
		ret = "[Q"
		if (len(self.queue) == 0):
			return ret+" <empty>]"

		for p in self.queue:
			ret+=" "+p.uID
		ret+="]"
		return ret

class cpuFCFS(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)
		self.cpuType = "FCFS"

	def update(self, time):
		remove = []
		for w in self.wait:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				remove.append(w)
				self.queue.append(w)
				self.wait.remove(w)
				w.ioBurstFinished()

		if len(self.queue) > 0:
			r = self.queue[0]
			r.cpuBursts[0] -=1
			if r.cpuBursts[0] == 0:
				r.cpuBurstFinished()
				self.queue.remove(r)
				if not r.isDone(time):
					self.wait.append(r)
				else:
					return self.contextSwitch + 1
		return 1

	def add(self, process):
		self.queue.append(process)
		return 1

class cpuSJF(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)
		self.type = "SJF"

	def update(self, time):
		pass

	def add(self, process):
		self.queue.append(process)
		self.queue = sorted(self.queue, key=lambda x: x.timeRemaining, reverse=False)
		return 1

class cpuSRT(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)
		self.type = "SRT"

	def update(self, time):
		pass

	def add(self, process):
		self.queue.append(process)
		self.queue = sorted(self.queue, key=lambda x: x.timeRemaining, reverse=False)
		return 1

class cpuRR(cpu):
	def __init__(self, contextSwitch, timeSlice):
		super().__init__(contextSwitch)
		self.type = "RR"
		self.timeSlice = timeSlice

	def update(self, time):
		pass

	def add(self, process):
		self.queue.append(process)
		return 1