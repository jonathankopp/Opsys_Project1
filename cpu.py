class cpu:
	def __init__(self, switchTime):
		self.running = None 	# Running process
		self.ready = []			# Ready processes
		self.wait = []			# I/0 blocked processes
		self.switchTime = switchTime	# Context switch time
		self.switching = 0		# keep track of time left switching
		# Simulation variables
		self.bursts = []		# keep track of all burst times for averaging
		self.switches = 0		# keep track of number of switches
		self.preemptions = 0	# keep track of numer of preemptions

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
	def __init__(self, switchTime):
		super().__init__(switchTime)
		self.cpuType = "FCFS"

	def update(self, time):
		# If no process if running context switch the next process in
		r = self.running
		if r is None:
			if len(self.ready) > 0:
				r = self.ready[0]
				print("time {}ms: Process {} started using CPU for {}ms burst {}".format(time, r.uID, r.cpuBursts[0], str(self)))
				self.running = r
				self.ready.remove(r)
				self.switching = self.switchTime
				self.switches += 1
				self.bursts.append(r.cpuBursts[0])
		# If process is switching decrement switch time
		wait = []
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
					print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, r.uID, len(r.cpuBursts), str(self)))
					self.running = None
					if not r.isDone(time):
						print("time {}ms: Process {} switching out of CPU; will block on I/O until time {} ".format(time, r.uID, time + r.ioBursts[0], str(self)))
						self.wait.append(r)
						wait.append(r)
		# Decrement time of everything in waiting
		for w in [w for w in self.wait if not w in wait]:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				print("time {}ms: Process {} completed I/0; added to ready queue {}".format(time, w.uID, str(self)))
				self.ready.append(w)
				self.wait.remove(w)

	def add(self, process):
		self.ready.append(process)
		return 1

class cpuSJF(cpu):
	def __init__(self, switchTime):
		super().__init__(switchTime)

	def update(self, time):
		pass

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: sum(x.cpuBursts))
		return 1

class cpuSRT(cpu):
	def __init__(self, switchTime):
		super().__init__(switchTime)

	def update(self, time):
		pass

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: x.timeRemaining, reverse=False)
		return 1

class cpuRR(cpu):
	def __init__(self, switchTime, timeSlice, rr):
		super().__init__(switchTime)
		self.timeSlice = timeSlice
		self.rr = rr # 'BEGINNING OR END'

	def update(self, time):
		pass

	def add(self, process):
		self.ready.append(process)
		return 1