import os
import sys
import threading

import page
import logEntry
from test._test_multiprocessing import exception_throwing_generator

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
		print("Initialize LogDispatcher with ", numOfLogs, 
			 " logs and the type of schedule is ", 
			               getScheduleTypeStr(typeOfSchedule))
		
	
	def updatePageVCs(self, pageId, vc):
		pageVector[pageId] = vc
		print("update vc of page ",pageId, " to ", vc)
		
	def addTxnEntryToLog(self, logId, logEty):
		logEtyList = entryToLogDict[logId]
		if logEtyList == NULL:
			logEtyList = list()
			entryToLogDict[logId] = logEtyList
		logEtyList.append(logEty)
			
	'''
	Figure out the placement plans
	@param[out] entryToLogDict: dict mapping log id 
	            to a list of log entries 
	'''
	def generateLogPlans(self, entryList):
		entryToLogDict = dict();
		if self.typeOfSchedule == 0:
			#random
			for logE in entryList:
				logId = logE.txnId % self.numOfLogs
				#obtain vc and update the log vc
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
		pass
	
	'''
	Distribute log entries to different logs
	@param[in] entryToLogDict: dict mapping log id to a list of 
	           log entries
	'''
	def sendEntriesToLogs(self, entryToLogDict):
		for logId in range(0, self.numOfLogs - 1):
			self.sendEntriesToLog(logId, entryToLogDict[logId])
			print('send to log ',logId, " entries: ", entryToLogDict[logId])
		