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

int  systemCall(string command);
void removeFile(string inputFileAddress);
void runPipeline(string Index, string patientID, string lane, string inputFastqFile1, string inputFastqFile2);
void runPipeline(string  Index, string patientID, vector<string> lanes, string directory);
void runPipeline(string patientID);
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
void MuTect(string normal_inputFile, string tumor_inputFile, string outputFile, string coverageFile, string analysisType);

