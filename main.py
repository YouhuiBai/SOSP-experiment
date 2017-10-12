import os
import sys
import time

import log
import logDispatcher
import txnExecutor

if __name__ == "__main__" :
	Log = log.Log()
	Logdisp = logDispatcher.LogDispatcher()
	file = open("trace.data")
	