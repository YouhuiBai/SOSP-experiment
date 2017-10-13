import os
import sys
import zmq
import threading

from page import *
from logEntry import *
from test._test_multiprocessing import exception_throwing_generator
from log import *
from _overlapped import NULL

def getScheduleTypeStr(t):
	if t == 0:
		return "Random"
	elif t == 1:
		return "Smart"
	else:
		print("Should not reach here!")
		sys.exit()

'''
This file contains functions associated with
LogDispatcher which is responsible for receiving
log entries from txnExecutors, making plans for
placing entries and sending plans to log handlers.
'''

class LogDispatcher :
	Queue = []
	mutex = threading.Condition()

	def __init__(self, numOfLogs, typeOfSchedule) :
		print("The LogDispatcher class")
		self.numOfLogs = numOfLogs
		self.typeOfSchedule = typeOfSchedule
		self.entryToLogDict = dict()
		self.logList = list()
		self.socketList = list()

		print("Initialize LogDispatcher with ", numOfLogs,
			 " logs and the type of schedule is ",
			               getScheduleTypeStr(typeOfSchedule))
		'''
		create log flush thread
		'''
		for i in range(self.numOfLogs) :
			indivLog = Log(i, self.numOfLogs)
			self.logList.append(indivLog)
			t = threading.Thread(target = indivLog.flushEntry, args = (i, ))
			t.setDaemon(True) # set the thread as Daemon thread
			t.start()
		for i in range(self.numOfLogs) :
			context = zmq.Context()
			socket = context.socket(zmq.PUB)
			socket.bind("tcp://127.0.0.1:500%d"%(i))
			self.socketList.append(socket)

	def addTxnEntryToLog(self, logId, logEty):
		logEtyList = self.entryToLogDict.get(logId)
		if logEtyList == None:
			logEtyList = list()
			self.entryToLogDict[logId] = logEtyList
		logEtyList.append(logEty)

	'''
	Figure out the placement plans
	@param[out] entryToLogDict: dict mapping log id
	            to a list of log entries
	'''
	def generateLogPlans(self, entryList):
		if self.typeOfSchedule == 0:
			#random
			for logE in entryList:
				logId = logE.txnId % self.numOfLogs
				#obtain the max of all pages' vc
				newVC = [0] * self.numOfLogs
				print(newVC)
				for pageId in logE.entryList:
					newVC = getMaxVC(newVC, pageVector[pageId])
					print(newVC)
				#obtain the max of the above vc and log vc
				self.logList[logId].increVCBit()
				newVC = getMaxVC(newVC, self.logList[logId].currentVC)
				print(newVC)

				#set log Entry vc and log vc and page vc
				logE.setVectorClock(newVC)
				self.logList[logId].setVectorClock(newVC)
				for pageId in logE.entryList:
					pageVector[pageId] = newVC.copy()
				self.addTxnEntryToLog(logId, logE)

			self.sendEntriesToLogs(self.entryToLogDict)
			self.entryToLogDict.clear()

		elif self.typeOfSchedule == 1:
			#smart
			print("Not implemented!")
			sys.exit()
		else:
			print("Should not reach here!")
			sys.exit()


	'''
    This function will figure out how to place
    a set of records on logs. It will be only triggered
    when one of the following two conditions matches:
    a) every 5 ms
    b) receiving every 10 entries
    '''
	def startAnalysis(self) :
		while True:
			LogDispatcher.mutex.acquire()
			while len(LogDispatcher.Queue) == 0:
				LogDispatcher.mutex.wait(0.001) #1ms
			self.generateLogPlans(LogDispatcher.Queue)
			LogDispatcher.Queue.clear()
			LogDispatcher.mutex.release()


	'''
	Send a list of entries to a specific log
	'''
	def sendEntriesToLog(self, logId, entryList):
		# call the log functions
		print("entrylist: ", entryList)
		self.socketList[logId].send_string(str(entryList))

	'''
	Distribute log entries to different logs
	@param[in] entryToLogDict: dict mapping log id to a list of
	           log entries
	'''
	def sendEntriesToLogs(self, entryToLogDict):
		for logId in range(0, self.numOfLogs):
			self.sendEntriesToLog(logId, entryToLogDict[logId])
			print('send to log ',logId, " entries: ", entryToLogDict[logId])