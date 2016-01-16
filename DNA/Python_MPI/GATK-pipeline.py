import time
from collections import OrderedDict
from subprocess import Popen
from multiprocessing import Pool
from itertools import chain, izip

bwa='bwa'
picardstem='/opt/NGS/picard-tools-1.119/'
gatkstem='/opt/NGS/GATK/GenomeAnalysisTK.jar'
java='java'
javatmp='-Djava.io.tmpdir=/tmp'
Xmxmarkdup='-Xmx8G'
Xmxsortsam='-Xmx8G'
Xmxbamindex='-Xmx8G'
Xmxrealign='-Xmx8G'
Xmxtarget='-Xmx8G'
Xmxbsqr='-Xmx8G'
Xmxrecal='-Xmx8G'

lanecores=4
bwacores=2

fastafile='/data/Annotation/GATK/hg19/ucsc.hg19.fasta'
vcffile='/data/Annotation/GATK/hg19/NA12878.HiSeq.WGS.bwa.cleaned.raw.subset.hg19.sites.vcf'
indelfile='/data/Annotation/GATK/hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf'
capturefile='/data/Annotation/GATK/Agilent/SureSelectExonV5+UTRs/S04380219_Covered.bed'


mypgms={'bwa':[bwa,'mem','-aM'],
     'markdup':[java,'-jar',Xmxmarkdup,javatmp,picardstem+'MarkDuplicates.jar'],
     'sortsam':[java,'-jar',Xmxsortsam,javatmp,picardstem+'SortSam.jar'],
     'bamindex':[java,'-jar',Xmxbamindex,javatmp,picardstem+'BuildBamIndex.jar'],
     'targets':[java,'-jar',Xmxtarget,javatmp,gatkstem,'-T','RealignerTargetCreator'],
     'realign':[java,'-jar',Xmxrealign,javatmp,gatkstem,'-T','IndelRealigner'],
     'bqsr':[java,'-jar',Xmxbsqr,javatmp,gatkstem,'-T','BaseRecalibrator'],
     'printreads':[java,'-jar',Xmxrecal,javatmp,gatkstem,'-T','PrintReads']}

myreffiles={'fasta':fastafile,
          'vcf':vcffile,
          'indel':indelfile,
          'capture':capturefile}

mymiscargs={'sortsam':[],'align':[],'realign':['--filter_bases_not_stored'],'markdup':[],'realign':[],'targets':[],'bwa':['-t',1],'bqsr':[],'recal':[],'mergebams':['--read_filter','MappingQualityZero'],'lanecores':lanecores,'bwacores':bwacores}

sampleinfo=OrderedDict()
sampleinfo.update({'CF33C':{'lanes':{'L001':{'input':['CF33C.L001.1','CF33C.L001.2']},'L002':{'input':['CF33C.L001.1','CF33C.L001.2']}}}})
sampleinfo.update({'CF33P':{'lanes':{'L001':{'input':['CF33P.L001.1','CF33P.L001.2']},'L002':{'input':['CF33P.L001.1','CF33P.L001.2']}}}})


def outlabs(sample,lane):
    stemfile=sample+'-'+lane
    sam=stemfile+'.sam'
    sortbam=stemfile+'-sort.bam'
    dupbam=stemfile+'-markdup.bam'
    metric=stemfile+'-metric.txt'
    realign=stemfile+'-realigned.bam'
    interval=stemfile+'-realign.intervals'
    recaltab=stemfile+'-recaltab.txt'
    recalbam=stemfile+'-recal.bam'
    out=OrderedDict()
    out.update({'output':{'sam':sam,'sortbam':sortbam,'dupbam':dupbam,'metric':metric,'interval':interval,'realign':realign,'recaltab':recaltab,'recalbam':recalbam}})
    return out

def makedesign(sampleinfo):
    for sample in sampleinfo.keys():
        for lane in sampleinfo[sample]['lanes'].keys():
            sampleinfo[sample]['lanes'][lane].update(outlabs(sample,lane))
        sampleinfo[sample].update({'merged': outlabs(sample,'merged')})
    
    return sampleinfo

makedesign(sampleinfo)

def GATKcall(mycall,stem):
    #print mycall
    #Popen(mycall,stdout=open(stem+'.stdout','w'),stderr=open(stem+'.stderr','w')).wait()
    print mycall

def align(f1,f2,outsam,sample,lane,pgm,reffile,misc):
    RG="@RG\tID:"+sample+"."+lane+"\tSM:"+sample+"\tPL:ILLUMINA"
    mycall=pgm['bwa']+misc['bwa']+['-R',RG,reffile['fasta'],f1,f2,'>',outsam]
    GATKcall(mycall,outsam)

    
def sortsam(insam,outbam,pgm,reffile,misc):
    mycall=pgm['sortsam']+['I='+insam,'O='+outbam,'SO=coordinate']+misc['sortsam']
    GATKcall(mycall,outbam)

def markdup(inbam,outbam,metric,pgm,reffile,misc):
    mycall=pgm['markdup']+['I='+inbam,'O='+outbam,'M='+metric]+misc['markdup']
    GATKcall(mycall,outbam)

def bamindex(pgm,inbam):
    mycall=pgm['bamindex']+['I='+inbam,'O=',]+misc
    GATKcall(mycall,'bamindex')

def targets(inbam,intervals,pgm,reffile,misc):
    mycall=pgm['realign']+['-R',reffile['fasta'],'-I',inbam,'--known',reffile['indel']]
    mycall=mycall+['-o',intervals]+misc['targets']
    GATKcall(mycall,intervals)
    
def realign(inbam,outbam,intervals,pgm,reffile,misc):
    mycall=pgm['realign']+['-R',reffile['fasta'],'--known',reffile['indel']]
    mycall=mycall+['-targetIntervals',intervals,'-I',inbam,'-o',outbam]+misc['realign']
    GATKcall(mycall,'log/indel')

def bqsr(inbam,recaltab,pgm,reffile,misc):
    mycall=pgm['bqsr']+['-R',reffile['fasta'],'-I',inbam]
    mycall=mycall+['-knownSites',reffile['indel'],'-knownSites',reffile['vcf']]
    mycall=mycall+['-L',reffile['capture'],'-o',recaltab]+misc['bqsr']
    GATKcall(mycall,recaltab)

def recal(inbam,outbam,recaltab,pgm,reffile,misc):
    mycall=pgm['printreads']+['-R',reffile['fasta'],'-I',inbam,'-BQSR',recaltab,'-o',outbam]+misc['recal']
    GATKcall(mycall,outbam)

def mergebams(inbams,outbam,pgm,reffile,misc):
    mycall=pgm['printreads']+['-R',reffile['fasta'],inbams,'-o',outbam]+misc['mergebams']
    GATKcall(mycall,outbam)

def GATKlane((sample,lane,stemdir,mydesign,pgm,reffile,miscarg)):
    directory=stemdir+lane+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory+'log/')
    mylane=mydesign[sample]['lanes'][lane]
    f1=mylane['input'][0]
    f2=mylane['input'][1]
    sam=directory+mylane['output']['sam']
    sortbam=directory+mylane['output']['sortbam']
    dupbam=directory+mylane['output']['dupbam']
    metric=directory+mylane['output']['metric']
    interval=directory+mylane['output']['interval']
    realignbam=directory+mylane['output']['realign']
    recalbam=directory+mylane['output']['recalbam']
    recaltab=directory+mylane['output']['recaltab']
    align(f1,f2,sam,sample,lane,pgm,reffile,miscarg)
    sortsam(sam,sortbam,pgm,reffile,miscarg)
    markdup(sortbam,dupbam,metric,pgm,reffile,miscarg)
    targets(dupbam,interval,pgm,reffile,miscarg)
    realign(dupbam, realignbam,interval,pgm,reffile,miscarg)
    bqsr(realignbam,recaltab,pgm,reffile,miscarg)
    recal(realignbam,recalbam,recaltab,pgm,reffile,miscarg)


GATKlane(('CF33C','L001',sampleinfo,mypgms,myreffiles,mymiscargs))

def GATKsample(sample,mydesign,stemdir,pgm,reffile,miscarg):
    directory=stemdir+sample
    if not os.path.exists(directory):
        os.makedirs(directory)
    lanes=mydesign[sample]['lanes'].keys()
    numlanes=len(lanes)
    cores=min(miscarg['lanecores'],numlanes)
    pools=Pool(processes=cores)
    #pools.map(GATKlane,[(sample,lane,mydesign,pgm,reffile,miscarg) for lane in  mydesign[sample]['lanes'].keys()])
    pools.close()
    l1=[mydesign[sample]['lanes'][lane]['output']['recalbam'] for lane in lanes]
    
    lanebams=list(chain.from_iterable(izip(['-I']*numlanes,l1)))
    
    outbam=mydesign[sample]['merged']['output']['sortbam']
    dupbam=mydesign[sample]['merged']['output']['dupbam']
    metric=mydesign[sample]['merged']['output']['metric']
    interval=mydesign[sample]['merged']['output']['interval']
    realignbam=mydesign[sample]['merged']['output']['realign']
    recalbam=mydesign[sample]['merged']['output']['recalbam']
    recaltab=mydesign[sample]['merged']['output']['recaltab']
    mergebams(lanebams,outbam,pgm,reffile,miscarg)
    markdup(outbam,dupbam,metric,pgm,reffile,miscarg)
    targets(dupbam,interval,pgm,reffile,miscarg)
    realign(dupbam, realignbam,interval,pgm,reffile,miscarg)
    bqsr(realignbam,recaltab,pgm,reffile,miscarg)
    recal(realignbam,recalbam,recaltab,pgm,reffile,miscarg)
    

GATKsample('CF33C',sampleinfo,'/data1/foo/',mypgms,myreffiles,mymiscargs)
