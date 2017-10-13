import os
import sys
import zmq
import threading

import page
import logEntry
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
	mutex = threading.Lock()

	def __init__(self, numOfLogs, typeOfSchedule) :
		print("The LogDispatcher class")
		self.numOfLogs = numOfLogs
		self.typeOfSchedule = typeOfSchedule
		self.entryToLogDict = dict()
		self.logList = list()
		print("Initialize LogDispatcher with ", numOfLogs,
			 " logs and the type of schedule is ",
			               getScheduleTypeStr(typeOfSchedule))
		'''
		create log flush thread
		'''
		for i in range(self.numOfLogs) :
			indivLog = Log(i, self.numOfLogs)
			self.logList.append(indivLog)
			t = threading.Thread(target = indivLog.flushEntry, args = (logId, ))
			t.serDaemon(True) # set the thread as Daemon thread
			t.start()


	def updatePageVCs(self, pageId, vc):
		pageVector[pageId] = vc
		print("update vc of page ",pageId, " to ", vc)

	def addTxnEntryToLog(self, logId, logEty):
		logEtyList = self.entryToLogDict[logId]
		if logEtyList == NULL:
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
				for pageId in logE.entryList:
					newVC = getMaxVC(newVC, pageVector[pageId])
				#obtain the max of the above vc and log vc
				self.logList[logId].increVCBit()
				newVC = getMaxVC(newVC, self.logList[logId].currentVC)
				
				#set log Entry vc and log vc and page vc
				logE.setVectorClock(newVC)
				self.logList[logId].setVectorClock(newVC)
				for pageId in logE.entryList:
					pageVector[pageId] = newVC.copy()
				self.addTxnEntryToLog(logId, logE)
		elif self.typeOfSchedule == 1:
			#smart
			print("Not implemented!")
			sys.exit()
		else:
			print("Should not reach here!")
			sys.exit()

		return entryToLogDict

	'''
    This function will figure out how to place
    a set of records on logs. It will be only triggered
    when one of the following two conditions matches:
    a) every 5 ms
    b) receiving every 10 entries
    '''
	def analysis(self) :
		pass

	'''
	Send a list of entries to a specific log
	'''
	def sendEntriesToLog(self, logId, entryList):
		# call the log functions
		context = zmq.Context()
		socket = context.socket(zmq.PUB)
		socket.bind("tcp://127.0.0.1:5000")
		# logEntry = input('input your data:')
		print(entryList)
		socket.send(entryList)

	'''
	Distribute log entries to different logs
	@param[in] entryToLogDict: dict mapping log id to a list of
	           log entries
	'''
	def sendEntriesToLogs(self, entryToLogDict):
		for logId in range(0, self.numOfLogs - 1):
			self.sendEntriesToLog(logId, entryToLogDict[logId])
			print('send to log ',logId, " entries: ", entryToLogDict[logId])