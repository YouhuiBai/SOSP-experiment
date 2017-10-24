import os
import sys
import datetime

if __name__ == "__main__" :
	logNum = [2, 4, 8]
	f = open("result", "a")
	for ln in logNum :
		for thr in range(4, 32, 4) :
			for time in range(10) :
				outFile = [str(ln), str(thr), str(time)]
				startTime = datetime.datetime.now()
				cmd = "python3 simulator.py %(t)d %(l)d %(n)s 600000"%({"t" : thr, "l" : ln, "n" : "-".join(outFile)})
				os.system(cmd)
				endTime = datetime.datetime.now()
				output = [str(ln), str(thr), str(time), str((endTime - startTime).seconds)]
				f.write(",".join(output))
				f.write("\n")
				f.flush()
				cmd = "rm -f *.log"
				os.system(cmd)
				print("output in run script:", ln, thr, time)
	f.close()
