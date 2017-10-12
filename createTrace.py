import os
import sys

if __name__ == "__main__" :
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fp1 = open(filein)
	fp2 = open(fileout, "w")
	for line in fp1 :
		l = line.split(",")
		if l[3] == 'w' or l[3] == 'W' :
			address = int(l[1])
			address //= 8
			fp2.write(",".join([l[0], str(address)]))
			fp2.write("\n")
	fp1.close()
	fp2.close()
