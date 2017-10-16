import threading
import page
from logDispatcher import *
import linecache
import random
from logEntry import *


class TxnExecutor :
	def __init__(self) :
		# print("The TxnExecutor class")
		pass

	def commit(self, txn, line1, line2 = "") :
		LogDispatcher.mutex.acquire()

		if not line2 == "" :
			logentry = LogEntry(int(txn), line1, line2)
		else :
			logentry = LogEntry(int(txn), line1)
		LogDispatcher.Queue.append(logentry)

		#check the length of queue
		#if queue is larger than 20 notify
		LogDispatcher.mutex.release()

	def executor(self, id) :
		countLines = 0 #count read lines of the current executor
		countCom = 0 #count committed transaction number

		#read one trace record. implemented in main
		bound = page.tracelines // page.workerNum // 2 #the number of times each executor reads
		# print("bound: %d"%(bound)) #debug
		for i in range(bound) :
			countLines += 2
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
			countCom += 1
		# print("executor%d read %d lines"%(id, countLines)) #debug
		# print("executor%d commit %d Txns"%(id, countCom)) #debug
		#prepare a log entry and send the log entry to logDispatcher queue





