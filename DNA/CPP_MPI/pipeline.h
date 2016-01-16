#include <time.h>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include "config.h"

using namespace std;

/*const string outputDIR = "Output/";

//# Reference File
const string data = "/home/abahman/Tools/Tools/data/";
const string FASTA = data + "hg19/ucsc.hg19.fasta";
const string KNOWNVCF = data + "hg19/NA12878.HiSeq.WGS.bwa.cleaned.raw.subset.hg19.sites.vcf";
const string KNOWNINDEL = data + "hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf";
const string CAPTURE= data + "S04380219_Covered.bed";

//# Memory
const string XmxMarkDUP="-Xmx8G";
const string XmxSortSAM="-Xmx8G";
const string XmxBAMIndex="-Xmx8G";
const string XmxRealign="-Xmx4G";
const string XmxRealignTarget="-Xmx2G";
const string XmxRecalib="-Xmx4G";
const string XmxPrintReads="-Xmx2G";
const string XmxCombine="-Xmx4G";

//# Programs
const string tool = "/home/abahman/Tools/Tools/";
const string bwa = tool + "bwa.kit/bwa";
const string sortsam = tool + "picard-tools-1.119/SortSam.jar";
const string markdup = tool + "picard-tools-1.119/MarkDuplicates.jar";
const string buildbamindex = tool + "picard-tools-1.119/BuildBamIndex.jar";
const string gatk = tool + "GenomeAnalysisTK.jar";

const int bwacore=10;

const string DES_CSV = "des.csv";
const string PL = "ILLUMINA"; //Platform/technology
*/
int  systemCall(string command);
void removeFile(string inputFileAddress);
void runPipeline(string Index, string patientID, string lane, string inputFastqFile1, string inputFastqFile2);
void runPipeline(string  Index, string patientID, vector<string> lanes, string directory);
string createRG(string patientID, string laneID);
void bwaCall(string rg, string inputFasta, string inputFastqFile1, string inputFastqFile2, string outputSAMFile);
void sortSAM(string inputSAMFile, string outputBAMFileSort, string OP, string MISC);
void markDuplicates( string inputBAMFile, string outputBAMFileSortDUP, string metricFile, string MISC);
void buildBAMIndex(string in_outBAMFileSortDUP, string MISC);
void GATKIndelRealigner(string inputFasta, string inutBAMFileSortDUP, string knownIndelFile, string realignIntFile, string outputBAMFileRealigned, string MISC);
void GATKBaseRecalibrator(string inputFasta, string inputBAMFileRealigned, string knownVCF, string knownIndel, string realignInt, string recalTableFile, string MISC); 
void GATKRealignerTargetCreator(string inputFasta, string inutBAMFileSortDUP, string knownIndelFile, string realignIntFile, string MISC);
void GATKPrintReads(string FASTA, string BAMFileRealigned,  string recalTableFile, string recalBAM, string MISC);	
void GATKCombine(string inputFasta, string output, string recalBAMs, string MISC);
void testMkdir(string inputFilename);
int checkFileExists(string filename);

