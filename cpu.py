
class cpu:
	def __init__(self, switchTime, alpha):
		self.running = None 	# Running process
		self.ready = []			# Ready processes
		self.wait = []			# I/0 blocked processes
		self.switchTime = switchTime	# Context switch time
		self.switchInTime = 0		# keep track of time left switching
		self.switchOutTime = 0
		self.switchingIn = None
		self.switchingOut = None
		# Simulation variables
		self.switches = 0		# keep track of number of switches
		self.preemptions = 0	# keep track of numer of preemptions
		# Variables for recalculating tau
		self.alpha = alpha
		# Added variable for single process

	def isDone(self):
		if len(self.ready) == 0 and len(self.wait) == 0 and self.running is None and self.switchInTime == 0 and self.switchOutTime == 0:
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
		if self.switchOutTime > 0:
			self.switchOutTime -= 1
			if self.switchOutTime == 0:
				if not self.switchingOut is None:
					self.wait.append(self.switchingOut)
				self.switchingOut = None
				if self.switchingIn is None:
					if len(self.ready) > 0:
						self.switchInTime = self.switchTime // 2
						self.switchingIn = self.ready[0]
						self.ready.remove(self.switchingIn)
		elif self.switchInTime > 0:
			self.switchInTime -= 1
			if self.switchInTime == 0:
				self.running = self.switchingIn
				self.switchingIn = None
				if time < 1000:
					print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, self.running.uID, self.running.cpuBursts[0], str(self)))
		# If process is not switching, decrement process burst time
		else:
			# If no process if running context switch the next process in
			r = self.running
			if r is None and self.switchingIn is None:
				if len(self.ready) > 0:
					self.switchInTime = self.switchTime // 2
					r = self.ready[0]
					self.switchingIn = r
					self.ready.remove(r)
					self.switches += 1
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switchOutTime = self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, r.uID, time+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.switchingOut = r
					else:
						print("time {}ms: Process {} terminated {}".format(time, r.uID, str(self)))
						self.switchingOut = None
		# Increment waiting for processes in ready queue
		for r in [r for r in self.ready if not r is self.switchingIn and not r is self.switchingOut]:
			r.waiting += 1
		# Decrement time of everything in waiting
		for w in sorted([w for w in self.wait if not w is self.switchingIn and not w is self.switchingOut], key=lambda x: x.uID):
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
		if self.switchOutTime > 0:
			self.switchOutTime -= 1
			if self.switchOutTime == 0:
				if not self.switchingOut is None:
					self.wait.append(self.switchingOut)
				self.switchingOut = None
				if self.switchingIn is None:
					if len(self.ready) > 0:
						self.switchInTime = self.switchTime // 2
						self.switchingIn = self.ready[0]
						self.ready.remove(self.switchingIn)
						self.switches += 1
		elif self.switchInTime > 0:
			self.switchInTime -= 1
			if self.switchInTime == 0:
				self.running = self.switchingIn
				self.switchingIn = None
				self.running.updateLastBurst()
				if time < 1000:
					print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, self.running.uID, self.running.cpuBursts[0], str(self)))
		# If process is not switching, decrement process burst time
		else:
			# If no process if running context switch the next process in
			r = self.running
			if r is None and self.switchingIn is None:
				if len(self.ready) > 0:
					self.switchInTime = self.switchTime // 2
					r = self.ready[0]
					self.switchingIn = r
					self.ready.remove(r)
					r.updateLastBurst()
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switchOutTime = self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						r.recalculateTau(self.alpha)
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Recalculated tau = {}ms for process {} {}".format(time, r.tau, r.uID, str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, r.uID, time+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.switchingOut = r
					else:
						print("time {}ms: Process {} terminated {}".format(time+1, r.uID, str(self)))
						self.switchingOut = None
		# Increment waiting for processes in ready queue
		for r in [r for r in self.ready if not r is self.switchingIn and not r is self.switchingOut]:
			r.waiting += 1
		# Decrement time of everything in waiting
		for w in sorted([w for w in self.wait if not w is self.switchingIn and not w is self.switchingOut], key=lambda x: x.uID):
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
		if self.switchOutTime > 0:
			self.switchOutTime -= 1
			if self.switchOutTime == 0:
				if not self.switchingOut is None:
					if self.switchingOut in self.preempted:
						self.add(self.switchingOut)
					else:
						self.wait.append(self.switchingOut)
				self.switchingOut = None
				if self.switchingIn is None:
					if len(self.ready) > 0:
						self.switchInTime = self.switchTime // 2
						self.switchingIn = self.ready[0]
						self.ready.remove(self.switchingIn)
						self.switches += 1
		elif self.switchInTime > 0:
			self.switchInTime -= 1
			if self.switchInTime == 0:
				self.running = self.switchingIn
				self.switchingIn = None
				if self.running in self.preempted:
					if time < 1000:
						print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(time, self.running.uID, self.running.cpuBursts[0], str(self)))
					self.preempted.remove(self.running)
				else:
					if time < 1000:
						print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, self.running.uID, self.running.cpuBursts[0], str(self)))
					self.running.updateLastBurst()
					self.burstDict[self.running.uID] = self.running.cpuBursts[0]
		else:
			# If no process if running context switch the next process in
			r = self.running
			if r is None and self.switchingIn is None:
				if len(self.ready) > 0:
					self.switchInTime = self.switchTime // 2
					r = self.ready[0]
					self.switchingIn = r
					self.ready.remove(r)
					r.updateLastBurst()
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1
				if r.cpuBursts[0] == 0:
					self.switchOutTime = self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						r.recalculateTau(self.alpha)
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Recalculated tau = {}ms for process {} {}".format(time, r.tau, r.uID, str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, r.uID, time+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.switchingOut = r
					else:
						print("time {}ms: Process {} terminated {}".format(time, r.uID, str(self)))
						self.switchingOut = None
		# Increment waiting for processes in ready queue
		for r in [r for r in self.ready if not r is self.switchingIn and not r is self.switchingOut]:
			r.waiting += 1
		# Decrement time of everything in waiting
		for w in sorted([w for w in self.wait if not w is self.switchingIn and not w is self.switchingOut], key=lambda x: x.uID):
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.add(w)
				self.wait.remove(w)
				# Handle preemptions
				if (not self.running is None) and (w.tau < self.running.tau - (self.burstDict[self.running.uID] - self.running.cpuBursts[0])):
					self.preemptions += 1
					self.switchOutTime = self.switchTime // 2
					self.preempted.append(self.running)
					self.switchingOut = self.running
					self.running = None
					if time < 1000:
						print("time {}ms: Process {} (tau {}ms) completed I/O and will preempt {} {}".format(time+1, w.uID, w.tau, self.switchingOut.uID, str(self)))
				else:
					if time < 1000:
						print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(time+1, w.uID, w.tau, str(self)))

	def add(self, process):
		self.ready.append(process)
		self.ready = sorted(self.ready, key=lambda x: (x.tau - (self.burstDict[x.uID] - x.cpuBursts[0]) if x in self.preempted else x.tau, x.uID))
		return 1

class cpuRR(cpu):
	def __init__(self, switchTime, alpha, timeSlice, rr):
		super().__init__(switchTime, alpha)
		self.cpuType = "RR"
		self.timeSlice = timeSlice
		self.timeSliceRemaining = timeSlice ##used to index timeslice
		self.rr = rr # 'BEGINNING OR END'
		self.preempted = []

	def update(self, time):
		# If process is switching decrement switch time
		if self.switchOutTime > 0:
			self.switchOutTime -= 1
			if self.switchOutTime == 0:
				if not self.switchingOut is None:
					if self.switchingOut in self.preempted:
						self.add(self.switchingOut)
					else:
						self.wait.append(self.switchingOut)
				self.switchingOut = None
				if self.switchingIn is None:
					if len(self.ready) > 0:
						self.switchInTime = self.switchTime // 2
						self.switchingIn = self.ready[0]
						self.ready.remove(self.switchingIn)
						self.switches += 1
		elif self.switchInTime > 0:
			self.switchInTime -= 1
			if self.switchInTime == 0:
				self.running = self.switchingIn
				self.switchingIn = None
				if self.running in self.preempted:
					self.preempted.remove(self.running)
				if time < 1000:
					print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, self.running.uID, self.running.cpuBursts[0], str(self)))
		# If process is not switching, decrement process burst time
		else:
			# If no process if running context switch the next process in
			r = self.running
			if r is None and self.switchingIn is None:
				if len(self.ready) > 0:
					self.switchInTime = self.switchTime // 2
					r = self.ready[0]
					self.switchingIn = r
					self.ready.remove(r)
			# If process is running (not None) decrement process burst time
			r = self.running
			if not r is None:
				r.cpuBursts[0] -=1 #decrement cpuBurst
				self.timeSliceRemaining -=1 #decrement timeslice					
				if r.cpuBursts[0] == 0: #cpu burst hits 0
					self.timeSliceRemaining = self.timeSlice #reset timeSliceRemaining
					self.switchOutTime =+ self.switchTime // 2
					r.cpuBurstFinished()
					self.running = None
					if not r.isDone(time):
						if time < 1000:
							print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, r.uID, len(r.cpuBursts), str(self)))
							print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, r.uID, time+r.ioBursts[0]+self.switchTime//2, str(self)))
						self.switchingOut = r
					else:
						print("time {}ms: Process {} terminated {}".format(time, r.uID, str(self)))				
						self.switchingOut = None
				elif self.timeSliceRemaining == 0: #if timeslice hits 0
					if r.cpuBursts[0] != 0: #There is a preemption because process didnt finish at same time
						if len(self.ready) == 0:
							if time < 1000:
								print("time {}ms: Time slice expired; no preemption because ready queue is empty {}".format(time, str(self)))	
						else:
							self.preemptions += 1 #increment preemption
							self.switchOutTime = self.switchTime // 2
							self.preempted.append(self.running)
							self.switchingOut = self.running
							self.running = None
							if time < 1000:
								print("time {}ms: Time slice expired; process {} preempted with {}ms to go {}".format(time, r.uID, r.cpuBursts[0], str(self)))
					self.timeSliceRemaining = self.timeSlice #reset timeSliceRemaining 
				
		# Increment waiting for processes in ready queue
		for r in [r for r in self.ready if not r is self.switchingIn and not r is self.switchingOut]:
			r.waiting += 1
		# Decrement time of everything in waiting
		for w in sorted([w for w in self.wait if not w is self.switchingIn and not w is self.switchingOut], key=lambda x: x.uID):
			w.ioBursts[0] -= 1
			#TODO: Tiebreakers for processes finishing at the same time
			if w.ioBursts[0] == 0:
				w.ioBurstFinished()
				self.add(w)
				self.wait.remove(w)
				if time < 1000:
					print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time+1, w.uID, str(self)))
					
	def add(self, process):
		if self.rr is "END":
			self.ready.append(process)
		else:
			self.ready = [process] + self.ready
		return 1