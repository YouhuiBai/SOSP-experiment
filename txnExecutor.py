import threading
import page
import logDispatcher
import linecache

class TxnExecutor :
	def __init__(self) :
		print("The TxnExecutor class")

	def commit(arg1, arg2) :
		

	def executor(self, onetrace, id) :
		#read one trace record. implemented in main
		bound = page.tracelines / page.workerNum // 2 #the number of times each executor reads
		for i in range(bound) :
			offset = (page.workerNum * i + id) * 2 # read the specific line for this executor
			line1 = linecache.getline("trace.data", offset)
			line2 = linecache.getline("trace.data", offset + 1)
			self.commit(line1, line2)

		#prepare a log entry and send the log entry to logDispatcher queue

		if iscommit() or queue is full :
			LogDispatcher.analysis()
			Log.flush()




