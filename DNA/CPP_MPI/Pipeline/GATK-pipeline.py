
import time
from collections import OrderedDict
from subprocess import Popen
from multiprocessing import Pool


picardstem='/opt/NGS/picard-tools-1.119/'
gatkstem='/opt/NGS/GATK/GenomeAnalysisTK.jar'
java='java'
Xmxmarkdup='-Xmx8G'
Xmxsortsam='-Xmx8G'
Xmxbamindex='-Xmx8G'
Xmxrealign='-Xmx8G'
Xmxindel='-Xmx8G'
Xmxbsqr='-Xmx8G'

pgm={'markdup':[java,'-jar',Xmxmarkdup,picardstem+'MarkDuplicates.jar'],
     'sortsam':[java,'-jar',Xmxsortsam,picardstem+'SortSam.jar'],
     'bamindex':[java,'-jar',Xmxbamindex,picardstem+'BuildBamIndex.jar'],
     'realign':[java,'-jar',Xmxrealign,gatkstem,'-T','RealignerTargetCreator'],
     'indel':[java,'-jar',Xmxindel,gatkstem,'-T','IndelRealigner'],
     'bsqr':[java,'-jar',Xmxbsqr,gatkstem,'-T','BaseRecalibrator']}

reffiles={'fasta':'/data/Annotation/GATK/hg19/ucsc.hg19.fasta',
          'vcf':'/data/Annotation/GATK/hg19/NA12878.HiSeq.WGS.bwa.cleaned.raw.subset.hg19.sites.vcf',
          'indel':'/data/Annotation/GATK/hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf',
          'capture':'/data/Annotation/GATK/Agilent/SureSelectExonV5+UTRs/S04380219_Covered.bed'}

sampleinfo={'CF33C':{'L001':['/ssddata/Patz/Reads/Sample_CF33C/CF33C_CGATGT_L001_R1_001.fastq.gz','CF33C_CGATGT_L001_R2_001.fastq.gz']},
            {'L002':['/ssddata/Patz/Reads/Sample_CF33C/CF33C_CGATGT_L002_R1_001.fastq.gz','CF33C_CGATGT_L002_R2_001.fastq.gz']},
            {'L003':['/ssddata/Patz/Reads/Sample_CF33C/CF33C_CGATGT_L003_R1_001.fastq.gz','CF33C_CGATGT_L003_R2_001.fastq.gz']},
            {'L004':['/ssddata/Patz/Reads/Sample_CF33C/CF33C_CGATGT_L004_R1_001.fastq.gz','CF33C_CGATGT_L004_R2_001.fastq.gz']}}

    


def GATKcall(mycall,stem):
    Popen(mycall,stdout=open(stem+'.stdout','w'),stderr=open(stem+'.stderr','w')).wait()


def sortsam(pgm,insam,outbam,misc):
    mycall=pgm['sortsam']+['I=',insam,'O='+procdir+outsam,'SO=coordinate']+misc
    GATKcall(mycall,'sortsam')

def markdup(pgm,inbam,outbam,metric,procdir,misc):
    mycall=pgm['markdup']+['I='+inbam,'O='+procdir+outbam,'M='+metric]+misc
    GATKcall(mycall,'markdup')

def bamindex(pgm,inbam):
    mycall=pgm['bamindex']+['I='+inbam,'O=',]+misc
    GATKcall(mycall,'bamindex')

def realign(pgm,reffiles,inbam,intervals,misc):
    mycall=pgm['realign']+['-R',reffiles['fasta'],'-I',inbam]'-known',reffiles['indel']]
    mycall=mycall+['-known',reffiles['indel'],'-o',intervals]+misc
    GATKcall(mycall,'log/indel')
    
def indel(pgm,reffiles,inbam,outbam,intervals,misc):
    mycall=pgm['indel']+['-R',reffiles['fasta'],'-known',reffiles['indel']]
    mycall=mycall+['-targetIntervals',intervals,'-I',inbam,'-o',outbam,'--filter_bases_not_stored']+misc
    GATKcall(mycall,'log/indel')

def bsqr(pgm,reffiles,inbam,recalfile,misc):
    mycall=pgm['bsqr']+['-R',fasta,'-I',inbam,'-knownSites',knownindel,'-knownSites',knownvcf]
    mycall=mycall+['-L',capture,'-o',recalfile]+misc
    GATKcall(mycall,'log/bsqr')


def GATKstep2(pgm,reffiles,sampleinfo,miscargs):
    sortsam(pgm,sampleinfo['samfile'],sampleinfo['sortbam'],miscargs['sortsam'])
    markdup(pgm,sampleinfo['sortbam'],sampleinfo['dedupbam'],sampleinfo['metric'],miscargs['markdup'])




java -jar $gatk -T IndelRealigner -R $fasta -I $bamfilesortdup -known $knownindel -targetIntervals $realignint  -o $bamfilerealigned --filter_bases_not_stored 


STEP 6 (Base Recalibration)
https://www.broadinstitute.org/gatk/gatkdocs/org_broadinstitute_gatk_tools_walkers_bqsr_BaseRecalibrator.php
java -jar $gatk  -T BaseRecalibrator -R $fasta -I $bamfilerealigned -knownSites $knownvcf -knownSites $knownindel -L $realignint -o $recaltable






         
bwa=/opt/NGS/bwa-0.7.12/bwa
sortsam=/opt/NGS/picard-tools-1.119/SortSam.jar
markdup=/opt/NGS/picard-tools-1.119/MarkDuplicates.jar
buildbamindex=/opt/NGS/picard-tools-1.119/BuildBamIndex.jar
gatk=/opt/NGS/GATK/GenomeAnalysisTK.jar


def GATKcall(mycall,stem):
    Popen(mycall,stdout=open(stem+'.stdout','w'),stderr=open(stem+'.stderr'))

