import os
import sys
import time
import threading
import datetime

import page
from txnExecutor import *
from logDispatcher import *

class Simulator :
	def __init__(self) :
		self.threadList = []
	def run(self, workerNum, logNum, outFile, tracelines) :
		#create logDispatcher
		logDisp = LogDispatcher(logNum, 0, outFile)
		threadOfLogDispatcher = threading.Thread(target = logDisp.startAnalysis, args = (tracelines, ))
		# threadOfLogDispatcher.setDaemon(True)
		threadOfLogDispatcher.start()

		for i in range(workerNum) :
			t = threading.Thread(target = TxnExecutor().executor, args = (i, tracelines, )) # executor per thread
			t.setDaemon(True)
			self.threadList.append(t)
			t.start()
		for t in self.threadList :
			t.join()



		# end the log thread(s)
		# for i in range(logNum) :
		# 	logDisp.socketList[i].send_string("end")
		for logthr in logDisp.logThread :
			logthr.join()

		threadOfLogDispatcher.join()
		print("run fun end")

if __name__ == "__main__" :

	S = Simulator()
	page.workerNum = int(sys.argv[1])
	page.logNum = int(sys.argv[2])
	outFile = str(sys.argv[3])
	tracelines = int(sys.argv[4])
	tracelines = tracelines // page.workerNum // 2 * 2 * page.workerNum
	print("tracelines in main:", tracelines)
	# startTime = datetime.datetime.now()
	S.run(page.workerNum, page.logNum, outFile, tracelines)
	# endTime = datetime.datetime.now()
	# print("run time:", (endTime-startTime).microseconds)
	print("main fun end")
