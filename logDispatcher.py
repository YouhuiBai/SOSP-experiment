import threading

class LogDispatcher :
	Queue = []
	mutex = threading.Lock()
	def __init__(self) :
		print("The LogDispatcher class")

	def analysis(self) :
		pass