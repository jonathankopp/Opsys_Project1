
class cpu:
	def __init__(self, switchTime, alpha):
		self.running = None 	# Running process
		self.ready = []			# Ready processes
		self.wait = []			# I/0 blocked processes
		self.switchTime = switchTime	# Context switch time
		self.switching = 0		# keep track of time left switching
		self.switchingOut = None
		# Simulation variables
		self.bursts = []		# keep track of all burst times for averaging
		self.switches = 0		# keep track of number of switches
		self.preemptions = 0	# keep track of numer of preemptions
		self.totals = []		# keep track of wait times TODO: This does not work
		# Variables for recalculating tau
		self.alpha = alpha

	def isDone(self):
		if(len(self.ready) == 0 and len(self.wait) == 0) and self.running is None and self.switchingOut is None and self.switching == 0:
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
	def __init__(self, switchTime, alpha):
		super().__init__(switchTime, alpha)
		self.cpuType = "FCFS"

	def update(self, time):
		# If process is switching decrement switch time
		if self.switching > 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			self.switchingOut = None
			# If no process if running context switch the next process in
			r = self.running
			if r is None:
				if len(self.ready) > 0:
					r = self.ready[0]
					self.running = r
					self.ready.remove(r)
					if time < 1000:
						print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time + self.switchTime//2, r.uID, r.cpuBursts[0], str(self)))
					self.switching =+ self.switchTime // 2
					self.switches += 1
					self.bursts.append(r.cpuBursts[0])
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switching =+ self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time+1, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time+1, r.uID, time+1+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.wait.append(r) ## TODO: Process should not be added to wait until it is finished switching out
						self.switchingOut = r
					else:
						self.totals.append(time - r.arrivalTime)
						print("time {}ms: Process {} terminated {}".format(time+1, r.uID, str(self)))
		# Decrement time of everything in waiting
		for w in [w for w in self.wait if not w is self.switchingOut]:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.ready.append(w)
				self.wait.remove(w)
				if time < 1000:
					print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time+1, w.uID, str(self)))

	def add(self, process):
		self.ready.append(process)
		return 1

class cpuSJF(cpu):
	def __init__(self, switchTime, alpha):
		super().__init__(switchTime, alpha)
		self.cpuType = "SJF"

	def update(self, time):
		# If process is switching decrement switch time
		if self.switching > 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			self.switchingOut = None
			# If no process if running context switch the next process in
			r = self.running
			if r is None:
				if len(self.ready) > 0:
					r = self.ready[0]
					self.running = r
					self.ready.remove(r)
					if time < 1000:
						print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time + self.switchTime//2, r.uID, r.cpuBursts[0], str(self)))
					self.switching =+ self.switchTime // 2
					self.switches += 1
					self.bursts.append(r.cpuBursts[0])
					r.updateLastBurst()
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switching =+ self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						r.recalculateTau(self.alpha)
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time+1, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Recalculated tau = {}ms for process {} {}".format(time+1, r.tau, r.uID, str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time+1, r.uID, time+1+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.wait.append(r) ## TODO: Process should not be added to wait until it is finished switching out
						self.switchingOut = r
					else:
						self.totals.append(time - r.arrivalTime)
						print("time {}ms: Process {} terminated {}".format(time+1, r.uID, str(self)))
		# Decrement time of everything in waiting
		for w in [w for w in self.wait if not w is self.switchingOut]:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.add(w)
				self.wait.remove(w)
				if time < 1000:
					print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(time+1, w.uID, w.tau, str(self)))

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: (x.tau, x.uID))
		return 1

class cpuSRT(cpu):
	def __init__(self, switchTime, alpha):
		super().__init__(switchTime, alpha)
		self.cpuType = "SRT"
		self.preempted = []
		self.burstDict = {}

	def update(self, time):
		# If process is switching decrement switch time
		if self.switching > 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			self.switchingOut = None
			# If no process if running context switch the next process in
			r = self.running
			if r is None:
				if len(self.ready) > 0:
					r = self.ready[0]
					self.running = r
					self.ready.remove(r)
					if r in self.preempted:
						if time < 1000:
							print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(time + self.switchTime//2, r.uID, r.cpuBursts[0], str(self)))
						self.preempted.remove(r)
					else:
						if time < 1000:
							print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time + self.switchTime//2, r.uID, r.cpuBursts[0], str(self)))
						self.burstDict[r.uID] = r.cpuBursts[0]
					self.switching =+ self.switchTime // 2
					self.switches += 1
					self.bursts.append(r.cpuBursts[0])					
					r.updateLastBurst()
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switching =+ self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						r.recalculateTau(self.alpha)
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time+1, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Recalculated tau = {}ms for process {} {}".format(time+1, r.tau, r.uID, str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time+1, r.uID, time+1+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.wait.append(r) ## TODO: Process should not be added to wait until it is finished switching out
						self.switchingOut = r
					else:
						self.totals.append(time - r.arrivalTime)
						print("time {}ms: Process {} terminated {}".format(time+1, r.uID, str(self)))
		# Decrement time of everything in waiting
		for w in [w for w in self.wait if not w is self.switchingOut]:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.add(w)
				self.wait.remove(w)
				# Handle preemptions
				if (not self.running is None) and (w.tau < self.running.tau - (self.burstDict[self.running.uID] - self.running.cpuBursts[0])):
					self.preemptions += 1
					self.switching =+ self.switchTime // 2
					self.add(self.running)
					self.preempted.append(self.running)
					if time < 1000:
						print("time {}ms: Process {} (tau {}ms) completed I/O and will preempt {} {}".format(time+1, w.uID, w.tau, self.running.uID, str(self)))
					self.running = None
				else:
					if time < 1000:
						print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(time+1, w.uID, w.tau, str(self)))

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: (x.tau, x.uID))
		return 1

class cpuRR(cpu):
	def __init__(self, switchTime, alpha, timeSlice, rr):
		super().__init__(switchTime, alpha)
		self.cpuType = "RR"
		self.timeSlice = timeSlice
		self.rr = rr # 'BEGINNING OR END'

	def update(self, time):
		# If process is switching decrement switch time
		if self.switching > 0:
			self.switching -= 1
		# If process is not switching, decrement process burst time
		else:
			self.switchingOut = None
			# If no process if running context switch the next process in
			r = self.running
			if r is None:
				if len(self.ready) > 0:
					r = self.ready[0]
					self.running = r
					self.ready.remove(r)
					if time < 1000:
						print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time + self.switchTime//2, r.uID, r.cpuBursts[0], str(self)))
					self.switching =+ self.switchTime // 2
					self.switches += 1
					self.bursts.append(r.cpuBursts[0])
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switching =+ self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time+1, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time+1, r.uID, time+1+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.wait.append(r) ## TODO: Process should not be added to wait until it is finished switching out
						self.switchingOut = r
					else:
						self.totals.append(time - r.arrivalTime)
						print("time {}ms: Process {} terminated {}".format(time+1, r.uID, str(self)))
		# Decrement time of everything in waiting
		for w in [w for w in self.wait if not w is self.switchingOut]:
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.ready.append(w)
				self.wait.remove(w)
				if time < 1000:
					print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time+1, w.uID, str(self)))
					
	def add(self, process):
		self.ready.append(process)
		return 1