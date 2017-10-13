class LogEntry:
    def __init__(self):
        self.numOfPages = 0
        self.entryList = list()
        self.txnId = 0
        self.vc = NULL
        
    def __init__(self, tId, line1, line2=""):
        self.txnId = tId
        self.entryList = list()
        self.vc = NULL
        self.addOnePageUpdate(line1)
        if line2 != "":
            self.addOnePageUpdate(line1)
            
    def addOnePageUpdate(self, line):
        self.entryList.append(line)
        self.numOfPages++