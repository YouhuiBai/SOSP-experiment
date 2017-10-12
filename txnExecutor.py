import threading
import page
from logDispatcher import *
import linecache

class TxnExecutor :
	def __init__(self) :
		# print("The TxnExecutor class")
		pass

	def commit(self, line1, line2, txn) :
		LogDispatcher.mutex.acquire()

		logentry = [int(txn), int(line1)]
		LogDispatcher.Queue.append(logentry)
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
			# print(line1, line2) #debug
			self.commit(line1, line2, offset / 2)

		#prepare a log entry and send the log entry to logDispatcher queue





