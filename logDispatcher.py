import threading

'''
This file contains functions associated with
LogDispatcher which is responsible for receiving
log entries from txnExecutors, making plans for
placing entries and sending plans to log handlers.
'''

class LogDispatcher :
	Queue = []
	mutex = threading.Lock()
	def __init__(self) :
		print("The LogDispatcher class")

	def analysis(self) :
		pass