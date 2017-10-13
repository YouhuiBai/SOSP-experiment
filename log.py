import threading

class Log :
	def __init__(self) :
		print("The Log class")
	def writeEntry(self, logid, logentry) : # write one log entry to log file
		fp1 = open("%d.log"%(logid), "a") # output log entry to log file
		fp2 = open("%d.data"%(logid), "a") # output log entry to analysis file
		tmp = []
		for item in logentry :
			tmp.append(str(item))
		fp1.write(','.join(tmp))
		fp2.write(','.join(tmp))
		fp2.write('\n')
		fp2.close()
		fp1.close()

		fp = open("%d.log"%(logid), "ab")
		fp.write(b'\x00' * 8192) #write the redo and undo information, 8KB
		fp.write(b'\x0a') # a new line
		fp.flush()
		fp.close()
	def getLog(logid) :
		return open("%d.log"%(logid))