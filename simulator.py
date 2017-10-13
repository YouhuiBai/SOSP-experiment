import os
import sys
import time
import threading

import page
from txnExecutor import *
from logDispatcher import *

class Simulator :
	def __init__(self) :
		self.threadList = []
	def run(self, workerNum, logNum) :
		#create logDispatcher
		logDisp = LogDispatcher(logNum, 0)
		threadOfLogDispatcher = threading.Thread(target = logDisp.startAnalysis, args = ())
		# threadOfLogDispatcher.setDaemon(True)
		threadOfLogDispatcher.start()

		for i in range(workerNum) :
			t = threading.Thread(target = TxnExecutor().executor, args = (i, )) # executor per thread
			# t.setDaemon(True)
			self.threadList.append(t)
			t.start()
		# for t in self.threadList :
			# t.join()

if __name__ == "__main__" :
	S = Simulator()

	S.run(page.workerNum, page.logNum)

	'''
	f = open("output.data", "w")
	for q in LogDispatcher.Queue :
		f.write(str(q))
		f.write("\n")
	f.close()
	'''