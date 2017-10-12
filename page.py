import threading
# maxPage = 168955252 #the max page number in trace file
maxPage = 131218 # the max page number in test trace file
pageVector = [threading.Lock() for i in range(maxPage)]  #the content in list is the mutex flag for one page, multithreads contend the mutex

workerNum = 4 # the total worker number in system

# tracelines = count(open("trace.data").readlines()) #the total line in trace file
tracelines = 57334 # the total line in test trace file