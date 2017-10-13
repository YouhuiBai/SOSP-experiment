'''
compute the bit-wise maximum values of
two vector clocks
'''
def getMaxVC(vc1, vc2):
    newVC = [0] * len(vc1)
    for i in range(0, len(vc1)):
        newVC[i] = vc1[i] if vc1[i] > vc2[i] else vc2[i]
    return newVC

'''
Check if the first vector clock
is smaller than the second one
'''
def lessThan(vc1, vc2):
    for i in range(0, len(vc1)):
        if vc1[i] > vc2[i]:
            return False
    return True

class LogEntry:
    '''
    Every log entry will have a transaction id
    a list of pages modified
    a vector clock indicating dependencies
    '''
    def __init__(self):
        self.numOfPages = 0
        self.entryList = list()
        self.txnId = 0
        self.vc = None

    def __init__(self, tId, line1, line2=""):
        self.numOfPages = 0
        self.txnId = tId
        self.entryList = list()
        self.vc = None
        self.addOnePageUpdate(line1)
        if line2 != "":
            self.addOnePageUpdate(line2)

    def addOnePageUpdate(self, line):
        self.entryList.append(int(line))
        self.numOfPages += 1
    
    def setVectorClock(self, vc):
        assert lessThan(self.vc, vc) == True
        self.vc = vc.copy()

    def __str__(self):
        objStr = str(tId)
        for entry in self.entryList:
            objStr += "-" + str(entry) 
        for i in self.vc:
            objStr += "-" + str(i)
        return objStr