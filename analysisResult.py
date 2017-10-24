import os
import sys

if __name__ == "__main__" :
	f = open("result")
	fout = open("output.data", "w")

	logNum = [2, 4, 8]
	for ln in logNum :
		for thr in range(4, 32, 4) :
			avg = 0
			for time in range(10) :
				line = f.readline()
				avg += int(line.split(",")[3])
			avg /= 10
			fout.write(str(ln) + " " + str(thr) + " " + str(avg) + "\n")

	f.close()
	fout.close()