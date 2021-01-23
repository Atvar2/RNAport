# coding=utf-8
import xlrd
import sys,io,re,os
import subprocess
from utils.findFile import findFile
from  collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class readXLSHead(object):
	oldToNew   =dict()
	sampleGroup=defaultdict(list)
	diffGroup   =dict()
	clsPRJ      =dict()

class readXLS(readXLSHead):
	def __init__(self,prfFile,rename,diffMethod,indexdir,indexFiles):
		self.projectFile=prfFile
		self.rename     =rename
		self.diffMethod =diffMethod
		self.indexdir   =indexdir
		self.indexFiles  = indexFiles
	def getdiffGroup(self):
		wb     =xlrd.open_workbook(filename=self.projectFile)
		sheet1 = wb.sheet_by_index(0)
		flag=0
		sNameCol=0
		if self.rename:
			sNameCol=5
		else:
			sNameCol=3

		for i in range(sheet1.nrows):
			row=sheet1.row_values(i)[1:]
			if 'treat'  in  sheet1.row_values(i):
				flag=1
				continue
			if sheet1.row_values(i)[0].startswith('Scode')	:
				flag = 0

			if 'Control' in sheet1.row_values(i) and 'Treat' in sheet1.row_values(i):
				flag=2
				continue
			if  'Cstart' in sheet1.row_values(i):
				flag=3
				continue
			if  'Cend'  in sheet1.row_values(i):
				flag=0
			if sheet1.row_values(i)[0].startswith('Pdiff'):
				flag = 0
			if flag == 2:
				row=[x for x in row if x != '']
				st=0;ed=0;s=0
				N=int(len(row)/3)
				for diff in range(N):
					st=ed
					s+=3
					ed=s
					subEle=row[st:ed]
					self.diffGroup[subEle[0]]="%s&%s" % (subEle[1],subEle[2])
					print(subEle)
			if flag == 1:
				N=int(len(row)/sNameCol)
				st=0;ed=0;s=0
				for j  in range(N):
					st=ed
					s+=sNameCol
					ed=s
					subEle=row[st:ed]
					if len(subEle)!=5 or '' in subEle:
						continue
					#print(subEle)
					if self.rename:
						self.oldToNew[subEle[1]]=subEle[3]
						self.sampleGroup[subEle[4]].append(subEle[3])
					else:
						self.sampleGroup[subEle[3]].append(subEle[1])
			if flag == 3:
				row=sheet1.row_values(i)
				row = [x for x in row if x != '']
				if '例'  in row:continue
				Plist=row[1].split('+')
				self.clsPRJ[Plist[0]]=Plist[1]
	def getCandDiff(self):
		diffP=''
		diffG=''
		for index,p in self.diffGroup.items():
			if not diffP:
				diffP=p
			else: diffP=','+p

		for G,sampleList in  self.sampleGroup.items():
			sampleStr=','.join(sampleList)
			if not diffG:
				diffG=G+':'+sampleStr
			else:
				diffG=' '+ G +':'+sampleStr
		return diffP,diffG
	def getCluster(self):
		clusterPRJ=''
		for pIndex,prj in self.clsPRJ.items():
			lineList=prj.split('+')
			SCproject=''
			for i in lineList:
				SCproject=self.diffMethod+':'+self.diffGroup[i]+','
			SCproject=re.sub(',$','',SCproject)
			if SCproject:
				clusterPRJ=SCproject+' '
			else:
				clusterPRJ=SCproject
		return clusterPRJ
	################## Fo database index ######################################
	def databaseIndex(self):
		databaseFile=dict()
		databaseFile=findFile(self.indexdir,self.indexFiles)
		return databaseFile
