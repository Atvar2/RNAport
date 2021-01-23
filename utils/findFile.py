import os,subprocess
def findFile(directory,indexFiles):
	indexTodatabase=dict()
	for indexFile in indexFiles:
		print(indexFile)
		p=subprocess.Popen('find -L  {path}  -name   {fq}'.format(path=directory,fq=indexFile), stdout = subprocess.PIPE,stdin = subprocess.PIPE,shell=True)
		stdout,stderr=p.communicate()
		fileExt=stdout.decode('utf-8').rstrip()
		indexTodatabase[indexFile]=fileExt
	return  indexTodatabase

