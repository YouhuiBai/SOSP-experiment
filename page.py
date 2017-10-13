import threading
workerNum = 4 # the number of worker in system
logNum = 4 # the number of log in system

# maxPage = 168955252 #the max page number in trace file
maxPage = 131218 # the max page number in test trace file
pageMutex = [threading.Lock() for i in range(maxPage)]  #the content in list is the mutex flag for one page, multithreads contend the mutex

vector = [0] * logNum
pageVector = [vector for i in range(maxPage)] #the vector clock in page


# tracelines = count(open("trace.data").readlines()) #the total line in trace file
tracelines = 16 # the total line in test trace file