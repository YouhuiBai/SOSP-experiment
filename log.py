import threading
import zmq

class Log :
	def __init__(self, logId, logN) :
		# print("The Log class")
		self.length = 0
		self.logId = logId
		self.currentVC = [0] * logN

	def getLogLength(self):
		return self.length;

	def increLogLengthBy(self, delta):
		self.length += delta

	def increVCBit(self):
		self.currentVC[self.logId] += 1

	def setVectorClock(self, vc):
		self.currentVC = vc.copy()

	def flushEntry(self, logid, outFile) : # write one log entry to file

		context = zmq.Context()
		socket = context.socket(zmq.SUB)
		socket.connect("tcp://127.0.0.1:500%d"%(logid))
		socket.setsockopt_string(zmq.SUBSCRIBE,'')
		while True:
			logentry = socket.recv()
			#print("logentry:",logentry)
			if str(logentry) == "b'end'" :
				print("the write is end")
				break
			else :
				fp1 = open("%s-%d.log"%(outFile, logid), "a") # output log entry to log file
				fp2 = open("%s-%d.data"%(outFile, logid), "a") # output log entry to analysis file
				# tmp = list()
				# for item in logentry : # may need to change logentry from string to list
					# tmp.append(str(item))
				fp1.write(str(logentry))
				fp2.write(str(logentry))
				fp2.write('\n')
				fp2.close()
				fp1.close()

				fp = open("%s-%d.log"%(outFile, logid), "ab")
				fp.write(b'\x00' * 8192) #write the redo and undo information, 8KB
				fp.write(b'\x0a') # a new line
				fp.flush()
				fp.close()

	def getLog(self, logid) :
		return open("%s-%d.log"%(outFile, logid))
