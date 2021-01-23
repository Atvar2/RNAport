import os,sys

dir=sys.argv[1]
for i,j,k  in os.walk(dir):
	print(i,j,k)
