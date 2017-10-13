import os
import sys
import threading

import page

'''
This file contains functions associated with
LogDispatcher which is responsible for receiving
log entries from txnExecutors, making plans for
placing entries and sending plans to log handlers.
'''

class LogDispatcher :
	Queue = []
	mutex = threading.Lock()
	
	def __init__(self, numOfLogs) :
		print("The LogDispatcher class")
		self.numOfLogs = numOfLogs
		
	
	def updatePageVCs(self, pageId, vc):
		pageVector[pageId] = vc
		print("update vc of page ",pageId, " to ", vc)
	
	'''
	Figure out the placement plans
	@param[out] entryToLogDict: dict mapping log id 
	            to a list of log entries 
	'''
	def generateLogPlans(self, entryList):
		entryToLogDict = dict();
		#TODO: fill in functions
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
		