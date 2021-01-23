import re,os
import subprocess
class getRawctg(object):
    def __init__(self,dir,BMS,rawInputName):
        self.dir=dir
        self.BMS=BMS
        self.rawInputName=rawInputName
        self.samToLib=dict()
    def getSamToLib(self):
        BMSHandle=open(self.BMS,'rU')
        lines=BMSHandle.read().rstrip().split("\n")
        for line in lines:
            lineList=line.rstrip().split('\t')
            self.samToLib[lineList[2]]=lineList[1]
    def getRawList(self):
        self.getSamToLib()
        dirList=self.dir.split(',')
        fqList=[]
        for eDir in dirList:
          p=subprocess.Popen('find -L  {path}  -name   {fq}'.format(path=eDir,fq="*_1.fq.gz"), stdout = subprocess.PIPE,stdin = subprocess.PIPE,shell=True)
          stdout,stderr=p.communicate()
          eachFqList=stdout.decode('utf-8').split("\n")
          fqList+=eachFqList
        fqList=[x for x in fqList if x != '']
        outHand=open(self.rawInputName,'w')
        for fq1 in fqList:
            fq1Dir,fq1Name=os.path.split(fq1)
            Lane=fq1Dir.split('/')[-1]
            Lib=re.split(r'_',Lane)[-1]
            fq1Prefix=re.sub('_1.fq.gz','',fq1Name)
            readLength=os.popen('grep Length {rawDir}/{lane}.report'.format(rawDir=fq1Dir,lane=Lane))
            readLength=readLength.read()
            readLength=re.search('(\d+);\d+', readLength)
            readLength=readLength.group(1)
            totalBases=os.popen('grep TotalBases {rawDir}/{lane}.report'.format(rawDir=fq1Dir,lane=Lane)).read()
            totalBases=re.search('(\d+)',totalBases).group(1)
            fq1Name='{}/{}_1.fq.gz'.format(fq1Dir,fq1Prefix)
            fq2Name='{}/{}_2.fq.gz'.format(fq1Dir,fq1Prefix)
            fq='{},{}'.format(fq1Name,fq2Name)
            outString='%s\t%s\t%s\t%s\t370\t%s\n' % (self.samToLib[Lib],Lane,fq,readLength,totalBases)
            outHand.write(outString)
