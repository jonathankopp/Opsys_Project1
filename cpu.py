class cpu:
	def __init__(self, contextSwitch):
		self.running = None
		self.ready = []
		self.wait = []
		self.contextSwitch = contextSwitch
		self.switching = 0

	def isDone(self):
		if(len(self.ready) == 0 and len(self.wait) == 0) and self.running is None:
			return True
		return False

	# #will return the 0 index (front of the queue) and remove it from the queue
	# def pop(self):
	# 	if(len(self.ready) == 0):
	# 		return None
	# 	Q=[]
	# 	x = 0
	# 	ret = None
	# 	for p in self.ready:
	# 		if(x != 0):
	# 			Q.append(p)
	# 		else:
	# 			ret = p
	# 		x+=1
	# 	self.ready = Q
	# 	return ret


	# #if it is not in the queue it will return false
	# def inQueue(self, process):
	# 	for p in self.ready:
	# 		if(process.uID == p.uID):
	# 			return True
	# 	return False

	# #if id doesnt exsist it will return None	
	# def removeByID(self, uID):
	# 	Q = []
	# 	ret = None
	# 	for p in self.ready:
	# 		if(p.uID != uID):
	# 			Q.append(p)
	# 		else:
	# 			ret = p
	# 	self.ready = Q
	# 	return retdef

	def __str__(self):
		ret = "[Q"
		if (len(self.ready) == 0):
			return ret + " <empty>]"

		for p in self.ready:
			ret += " " + p.uID
		ret += "]"
		return ret

class cpuFCFS(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)
		self.cpuType = "FCFS"

	def update(self, time):
		# If no process if running context switch the next process in
		r = self.running
		if r is None:
			if len(self.ready) > 0:
				r = self.ready[0]
				print("time " + str(time) + "ms: Process " + r.uID + " started using CPU for " + str(r.cpuBursts[0]) + "ms burst " + str(self))
				self.running = r
				self.ready.remove(r)
				self.switching = self.contextSwitch
		# If process is switching decrement switch time
		if self.switching >= 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			r = self.running
			# If process is running (not None) decrement process burst time
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					r.cpuBurstFinished()
					print("time " + str(time) + "ms: Process " + r.uID + " completed a CPU burst; " + str(len(r.cpuBursts)) + " bursts to go " + str(self))
					self.running = None
					if not r.isDone(time):
						print("time " + str(time) + "ms: Process " + r.uID + " switching out of CPU; will block on I/O until time " + str(time + r.ioBursts[0]) + " " + str(self))
						self.wait.append(r)
		# Decrement time of everything in waiting
		for w in self.wait:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				print("time " + str(time) + "ms: Process " + w.uID + " completed I/0; added to ready queue " + str(self))
				self.ready.append(w)
				self.wait.remove(w)

	def add(self, process):
		self.ready.append(process)
		return 1

class cpuSJF(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)

	def update(self, time):
		# If no process if running context switch the next process in
		r = self.running
		if r is None:
			if len(self.ready) > 0:
				r = self.ready[0]
				print("time " + str(time) + "ms: Process " + r.uID + " started using CPU for " + str(r.cpuBursts[0]) + "ms burst " + str(self))
				self.running = r
				self.ready.remove(r)
				self.switching = self.contextSwitch
		# If process is switching decrement switch time
		if self.switching >= 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			r = self.running
			# If process is running (not None) decrement process burst time
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					r.cpuBurstFinished()
					print("time " + str(time) + "ms: Process " + r.uID + " completed a CPU burst; " + str(len(r.cpuBursts)) + " bursts to go " + str(self))
					self.running = None
					if not r.isDone(time):
						print("time " + str(time) + "ms: Process " + r.uID + " switching out of CPU; will block on I/O until time " + str(time + r.ioBursts[0]) + " " + str(self))
						self.wait.append(r)
		# Decrement time of everything in waiting
		for w in self.wait:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				print("time " + str(time) + "ms: Process " + w.uID + " completed I/0; added to ready queue " + str(self))
				self.ready.append(w)
				self.wait.remove(w)

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: sum(x.cpuBursts))
		return 1

class cpuSRT(cpu):
	def __init__(self, contextSwitch):
		super().__init__(contextSwitch)

	def update(self, time):
		pass

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: x.timeRemaining, reverse=False)
		return 1

class cpuRR(cpu):
	def __init__(self, contextSwitch, timeSlice):
		super().__init__(contextSwitch)
		self.timeSlice = timeSlice

	def update(self, time):
		pass

	def add(self, process):
		self.ready.append(process)
		return 1