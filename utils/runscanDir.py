#/*************************************************************************
# > File Name: runscanDir.py
# > Author: chenjunhui
# > Mail: chenjhbio@163.com 
#> Copyright (C): Tue 20 Mar 2018 05:53:44 PM CST. All rights reserved.
# ************************************************************************/
import sys,os,re
from optparse  import OptionParser
import time
import  stat 
from  stat  import  *
usage='''
	python  *.py  -d  dirlist   -r  .exe   
     '''
#  Recursion  paramat should be the same.
#
UID2USRENAME='/etc/passwd'

def setup_options():
	parser=OptionParser(usage=usage,version='version v1.0')
	parser.add_option('-d','--scandir',dest='SCANDIR',type=str,action='store', \
	help='dir list you will want to be scaned')
	parser.add_option('-r','--rmsuffix',dest='RMSF',action='append', \
	help='file suffix you want to remove from your dir, you can appoint more than one suffix')
	parser.add_option('-o','--output',dest='OT',action='store', default='output' ,\
	help='the files with suffix you provided!')
	parser.add_option('-a','--autormOE',dest='RMOE', \
	help='whether remvoe .sh.[oe] file, default remove all .sh.[oe] file in your provided dir!')
	(options,args)=parser.parse_args()
	return (options,args)
	
def uid2Name(*args):
	uid=args[0]
	try:
		UIdUsername=open(UID2USRENAME,'rU')
	except  IOError:
		raise  IOError("Can't open passwd file %s"  % UID2USRENAME)
	Iterstream=UIdUsername.xreadlines()
	for  line  in  Iterstream:
		line=line.strip()
		if  uid  in  line:
			lineList=re.split(r'\:',line)
			return lineList[0]
class index(object):
	def __init__(self,directory,tmpFile):
		self.directory=directory
		self.tmpFile=open(tmpFile,'a+')
	def  Recursion(self):   #Need  default value
		#st=os.stat(directory)
		#mode=st.st_mode
		if  not os.path.exists(self.directory):
			return
		
		elif    os.path.islink(self.directory):
			return 
		elif os.path.isfile(self.directory):
			self.tmpFile.write(self.directory+'\n')
		elif  os.path.isdir(self.directory):
			for subdir  in  os.listdir(self.directory):
				#directory=re.sub(r'\/$','',directory)
				self.directory=self.directory+'/'+subdir	
				self.Recursion()
index('/hwfswh2/BC_COM_P5/F19FTSCCWLJ2258/HICygxD/F20FTSCCKF1773_NICzjkE/00.ref/01.index','test.txt').Recursion()			
