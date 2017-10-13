import threading
import page
from logDispatcher import *
import linecache
import random


class TxnExecutor :
	def __init__(self) :
		# print("The TxnExecutor class")
		pass

	def commit(self, txn, line1, line2 = "") :
		LogDispatcher.mutex.acquire()

		logentry = [int(txn), int(line1)]
		LogDispatcher.Queue.append(logentry)
		if not line2 == "" :
			logentry = [int(txn), int(line2)]
			LogDispatcher.Queue.append(logentry)

		LogDispatcher.mutex.release()

	def executor(self, id) :
		#read one trace record. implemented in main
		bound = page.tracelines // page.workerNum // 2 #the number of times each executor reads
		# print("bound: %d"%(bound)) #debug
		for i in range(bound) :
			offset = (page.workerNum * i + id) * 2 # read the specific line for this executor
			# print("id: ", id, " offset: ", offset) #debug
			line1 = linecache.getline("trace.data", offset + 1)
			line2 = linecache.getline("trace.data", offset + 2)
			pagenum = random.randrange(1, 3, 1) # random number in [1, 2]
			if pagenum == 1 :
				if random.randrange(0, 2, 1) == 0 :
					linetmp = line1
				else : linetmp = line2
				self.commit(offset / 2, linetmp)
			elif pagenum == 2 :
				self.commit(offset  / 2, line1, line2)
		#prepare a log entry and send the log entry to logDispatcher queue





