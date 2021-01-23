import re,os
import click
from readProject.Forxlsx import readXLS
from readProject.rawData import getRawctg

@click.group(context_settings={'help_option_names':['-h','--help']})
@click.option(
    '--verbosity','-v',type=click.Choice(['info','debug']),
    default='info',help='Verbosity level, default=info.'
)
@click.option('--version', is_flag=True, help="Print version number")
def RNAPort(verbosity,version):
    '''
    Welcome to use the RNAKit for preparing config of RNA pipeline.
    :param verbosity:
    :param version:
    :return:
    Contact: chenjunhui@genomics.cn
    '''
    if version:
        print("This is RNAKit 0.1.0")

@RNAPort.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--rawdir', default='/zfswh4/solexa/homeward_A/homeward001A', help='path of raw data')
@click.option('--bmsinfo', default='sample2Library.txt', help='BMS information, format: code sample library')
@click.option('--outfile',default='RawData.list',help='output file')
def getdata(rawdir,bmsinfo,outfile):
    '''
    get raw data list for RNA reference pipeline
    '''

    rawDataObj=getRawctg(rawdir,bmsinfo,outfile)
    rawDataObj.getRawList()
    print('finished to obtain rawDataList %s' % outfile)

############## prepare for RNA ref config #####################################
@RNAPort.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('refconfig', nargs=1, type=click.Path(exists=True))
@click.option('--rawdir', default='/zfswh4/solexa/homeward_A/homeward001A', help='path of raw data')
@click.option('--bmsinfo', default='sample2Library.txt', help='BMS information, format: code sample library')
@click.option('--outfile',default='RawData.list',help='output file')
@click.option('--projectfile',default='test.xlsx',help='project file provided')
@click.option('--rename', is_flag=True, help='rename sample name in the project')
@click.option('--diffmethod',default='DEGseq',help='Gene Diff Expression method')
@click.option('--indexdir',default='./',help='directory of genome database index')
@click.option('--managermail',default='wangjingxian@genomics.cn',help='project manager email')
@click.option('--analysismail',default='chenjunhui@genomics.cn',help='Analysis email')
@click.option('--subcode',default='HICygxD',help='subcode of the project')
@click.option('--projectname',default='F20FTSCCKF1773',help='Project name')
@click.option('--speciename',default='species',help='specie Name')
@click.option('--group',default='pap',help='group of analysis')
@click.option('--queue',default='bc.q',help='queue of analysis')
@click.option('--cleandata',default='8',type=int,help='data size of clean data')
@click.option('--platform',default='BGISEQ-500',help='sequencing Platform')
def  rnarefcfg(refconfig,rawdir,bmsinfo,outfile,projectfile,rename,diffmethod, indexdir,managermail,analysismail,subcode,projectname,speciename,group,queue,cleandata,platform):
    '''
    indexFiles=['refMrna.fa','chrALL.fa.dict','chrALL.fa.1.ht2l','refMrna.gtf','refPep.fa','specie.nr.desc','gene2tr.txt']
    :param RNArefcfg:
    :param projectFile:
    :param rename:
    :param diffMethod:
    :param indexdir:
    :param managerMail:
    :param analysisMail:
    :param subCode:
    :param projectName:
    :param specieName:
    :param group:
    :param queue:
    :param CleanData:
    :param platForm:
    :return:
    '''
    indexFiles=['refMrna.fa','chrALL.fa.dict','chrALL.fa.1.ht2l','refMrna.gtf','refPep.fa','species.nr.desc','gene2tr.txt']
    if not os.path.exists(projectfile):
        return
    rawDataObj = getRawctg(rawdir, bmsinfo, outfile).getRawList()
    prjObj=readXLS(projectfile,rename,diffmethod,indexdir,indexFiles)
    databaseFiles=prjObj.databaseIndex()
    geneIndex=databaseFiles['refMrna.fa']
    GATKIndex=databaseFiles['chrALL.fa.dict'].replace('.dict','')
    gene2tr  =databaseFiles['gene2tr.txt']
    hisatIndex=databaseFiles['chrALL.fa.1.ht2l'].replace('.1.ht2l','')
    nrDesc=databaseFiles['species.nr.desc']
    annoIndex=re.sub('.nr.desc','',nrDesc)
    GOprefix=annoIndex
    koann=annoIndex+'.ko'
    gtf=databaseFiles['refMrna.gtf']
    pepIndex=databaseFiles['refPep.fa']
    cfgHandle=open(refconfig,'rU')
    cfgContent=cfgHandle.read()
    prjObj.getdiffGroup()
    hdRawlist=open(outfile,'rU')
    outList =open('rawListSampleold2New.txt','w')
    for i in hdRawlist.read().split('\n'):
        iList=i.rstrip().split('\t')
        if iList[0] in prjObj.oldToNew.keys():
            iList[0]=prjObj.oldToNew[iList[0]]
            outList.write('\t'.join(iList)+'\n')
    diffP,diffG=prjObj.getCandDiff()
    clusterPlan=prjObj.getCluster()
    cfgContent=re.sub('geneIndex',geneIndex,cfgContent)
    cfgContent=re.sub('GATKIndex',GATKIndex,cfgContent)
    cfgContent=re.sub('gene2tr',gene2tr,cfgContent)
    cfgContent=re.sub('hisatIndex',hisatIndex,cfgContent)
    cfgContent=re.sub('nrDesc',nrDesc,cfgContent)
    cfgContent=re.sub('GOprefix',GOprefix,cfgContent)
    cfgContent=re.sub('koann',koann,cfgContent)
    cfgContent=re.sub('gtf',gtf,cfgContent)
    cfgContent=re.sub('pepIndex',pepIndex,cfgContent)
    cfgContent=re.sub('managerMail',managermail,cfgContent)
    cfgContent=re.sub('analysisMail',analysismail,cfgContent)
    cfgContent=re.sub('diffGroup',diffG,cfgContent)
    cfgContent =re.sub('pairdiff',diffP,cfgContent)
    cfgContent =re.sub('clusterPlan',clusterPlan,cfgContent)
    cfgContent =re.sub('subcode',subcode,cfgContent)
    cfgContent =re.sub('projectname',projectname,cfgContent)
    cfgContent =re.sub('speciename',speciename,cfgContent)
    cfgContent =re.sub('cleandata',str(cleandata),cfgContent)
    cfgContent =re.sub('platform',platform,cfgContent)
    cfgContent =re.sub('queue',queue,cfgContent)
    with open ('input.config.txt','w')  as cfg:
        cfg.write(cfgContent)
############# prepare config for RNA denovo of bgi pipeline ##########################
@RNAPort.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('denovoconfig', nargs=1, type=click.Path(exists=True))
@click.option('--rawdir', default='/zfswh4/solexa/homeward_A/homeward001A', help='path of raw data')
@click.option('--bmsinfo', default='sample2Library.txt', help='BMS information, format: code sample library')
@click.option('--outfile',default='RawData.list',help='output file')
@click.option('--rename', is_flag=True, help='rename sample name in the project')
@click.option('--diffmethod',default='DEGseq',help='Gene Diff Expression method')
@click.option('--managermail',default='wangjingxian@genomics.cn',help='project manager email')
@click.option('--analysismail',default='chenjunhui@genomics.cn',help='Analysis email')
@click.option('--subcode',default='HICygxD',help='subcode of the project')
@click.option('--projectname',default='F20FTSCCKF1773_HICygxD',help='Project name')
@click.option('--speciename',default='species',help='specie Name')
@click.option('--group',default='pap',help='group of analysis')
@click.option('--queue',default='bc.q',help='queue of analysis')
@click.option('--cleandata',default='8',type=int,help='data size of clean data')
@click.option('--platform',default='BGISEQ-500',help='sequencing Platform')
def rnadenvo(denovoconfig,rawdir,bmsinfo,outfile,rename,diffmethod,managermail,analysismail,subcode,projectname,\
             speciename,group,queue,cleandata,platform):
    rawDataObj = getRawctg(rawdir, bmsinfo, outfile).getRawList()
    cfgHandle = open(denovoconfig, 'rU')
    cfgContent = cfgHandle.read()
    cfgContent = re.sub('subcode',subcode)
    cfgContent = re.sub('manager', managermail, cfgContent)
    cfgContent = re.sub('Analyst', analysismail, cfgContent)
    cfgContent = re.sub('diffGroup', diffG, cfgContent)
    cfgContent = re.sub('pairdiff', diffP, cfgContent)
    cfgContent = re.sub('projectname', projectname, cfgContent)
    cfgContent = re.sub('speciename', speciename, cfgContent)
    cfgContent = re.sub('cleandata', str(cleandata), cfgContent)
    cfgContent = re.sub('platform', platform, cfgContent)
    cfgContent = re.sub('queue', queue, cfgContent)
    with open('input.config.txt','w') as cfg:
        cfg.write(cfgContent)
if __name__ == '__main__':
    RNAPort()
