#include "pipeline.h" 


int  systemCall(string Command){

	struct timeval tim;
	gettimeofday(&tim, NULL);
	double t1=tim.tv_sec+(tim.tv_usec/1000000.0);

	char *sCommand = new char[Command.length() + 1];
	cout << "Command: " << Command << endl;
	strcpy(sCommand,Command.c_str());

	int val; 

#ifdef PRINT_COMMANDS
			val = 0; 
#else
			val = system(sCommand);
#endif

	gettimeofday(&tim, NULL);
	double t2=tim.tv_sec+(tim.tv_usec/1000000.0);
	printf("%.6lf seconds elapsed\n", t2-t1);
	

	return val;
}


void testMkdir(string inputFilename){

        if (checkFileExists(inputFilename) != 0 ){
                systemCall ("mkdir " + inputFilename);
        }
}

int checkFileExists(string filename){

        string SS = "[ -e " + filename +" ]";

        return  systemCall(SS);

}


void removeFile(string inputFileAddress){
	
	string SS = "rm " + inputFileAddress;
        systemCall(SS);
}

void runPipeline(string  Index, string patientID, vector<string> lanes, string directory) {

	string BAMFileSort, recalBAMs, BAMFileSortDUP, metricFile, BAMFileRealigned,  recalTableFile, recalBAM, MISC, RealignInt;
	
	string outputDIR = OutputDIR + patientID + "/";
	

	BAMFileSort=outputDIR + patientID + "-merged.bam";
	for(int i=0; i< lanes.size(); i++){
		recalBAMs = recalBAMs + " -I " + outputDIR + patientID+"_"+Index+"_"+ lanes[i] +"-recal.bam";
	}
	MISC="";
	/*STEP 7 Combine the four lanes*/
	GATKCombine(FASTA, BAMFileSort, recalBAMs, MISC);

	/*STEP 3 (Mark Duplicates)*/
	BAMFileSortDUP = outputDIR + patientID + "-merged-dedup.bam"; 
	metricFile = outputDIR + patientID + "-merged-metrics.txt";
	MISC = "";
	markDuplicates(BAMFileSort, BAMFileSortDUP, metricFile, MISC);
	
	/*STEP 4 (Index BAM file)*/
	MISC="";
	buildBAMIndex(BAMFileSortDUP, MISC);

	/*STEP 5 (Local Realignment)*/
	/*Step 5a: Create the targets*/
	MISC="";	
	RealignInt = outputDIR +  patientID +  "-merged-dedup-target.intervals"; 
	GATKRealignerTargetCreator(FASTA,  BAMFileSortDUP, KNOWNINDEL, RealignInt, MISC);

	/*Step 5b: Realign*/
	BAMFileRealigned = outputDIR + patientID + "-merged-dup-realign.bam";
	MISC = " --filter_bases_not_stored";
	GATKIndelRealigner(FASTA, BAMFileSortDUP, KNOWNINDEL, RealignInt, BAMFileRealigned, MISC);

	/*STEP 6 (Base Recalibration)*/
	/*Step 6a*/
	recalTableFile =outputDIR + patientID +  "-merged-recal-table.txt"; 
	MISC="";
	GATKBaseRecalibrator(FASTA, BAMFileRealigned, KNOWNVCF, KNOWNINDEL, CAPTURE, recalTableFile, MISC);

	/*STEP 6b*/
	recalBAM = outputDIR + patientID +  "-merged-recal.bam"; 
	MISC="";
	GATKPrintReads(FASTA, BAMFileRealigned,  recalTableFile, recalBAM, MISC);	

}



void runPipeline(string Index, string patientID, string lane, string inputFastqFile1, string inputFastqFile2){

	string readgroup, inputFasta, SAMFile, BAMFileSort, OP, MISC, BAMFileSortDUP, metricFile, BAMFileRealigned, recalTableFile, recalBAM, RealignInt;

	string outputDIR = OutputDIR + patientID + "/";
	
	/*Step 1 (Align Lane)*/
	readgroup = createRG(patientID, lane);  
	inputFasta = FASTA;
	SAMFile = outputDIR + patientID +"_"+ Index +"_"+ lane + ".sam";
	bwaCall(readgroup, inputFasta, inputFastqFile1, inputFastqFile2, SAMFile);


	/*Step 2 (Sort Lane)*/
	BAMFileSort = outputDIR + patientID +"_"+ Index +"_"+ lane + "-sort.bam";					
	OP = "coordinate";
	MISC = "";	
	sortSAM(SAMFile, BAMFileSort, OP, MISC);

	/*STEP 3 (Mark Duplicates)*/
	BAMFileSortDUP = outputDIR + patientID +"_"+ Index +"_"+ lane + "-sort-dup.bam";
	metricFile = outputDIR + patientID +"_"+ Index +"_"+ lane + "-dup-metrics.txt";
	MISC = "";
	markDuplicates(BAMFileSort, BAMFileSortDUP, metricFile, MISC);


	/*STEP 4 (Index BAM file)*/
	MISC="";
	buildBAMIndex(BAMFileSortDUP, MISC);

	/*STEP 5 (Local Realignment)*/
	/*Step 5a: Create the targets*/
	RealignInt = outputDIR + patientID +"_"+ Index +"_"+ lane + "-realign.intervals";
	MISC="";	
	GATKRealignerTargetCreator(FASTA,  BAMFileSortDUP, KNOWNINDEL, RealignInt, MISC);

	/*Step 5b: Realign*/
	BAMFileRealigned = outputDIR + patientID +"_"+ Index +"_"+ lane + "-sort-dup-realign.bam";
	MISC = " --filter_bases_not_stored";
	GATKIndelRealigner(FASTA, BAMFileSortDUP, KNOWNINDEL, RealignInt, BAMFileRealigned, MISC);

	/*STEP 6 (Base Recalibration)*/
	/*Step 6a*/
	recalTableFile = outputDIR + patientID +"_"+ Index +"_"+ lane + "-recal-table.txt"; 
	MISC="";
	GATKBaseRecalibrator(FASTA, BAMFileRealigned, KNOWNVCF, KNOWNINDEL, CAPTURE, recalTableFile, MISC);

	/*STEP 6b*/
	recalBAM = outputDIR + patientID +"_"+ Index +"_"+ lane + "-recal.bam"; 
	MISC="";
	GATKPrintReads(FASTA, BAMFileRealigned,  recalTableFile, recalBAM, MISC);	


}


void runPipeline(string patientID){

	string outputDIR_P = OutputDIR + patientID + "P/";
	string outputDIR_C = OutputDIR + patientID + "C/";

	string recalNormalBAM = outputDIR_C + patientID +"C-merged-recal.bam";   
	string recalTumorBAM = outputDIR_P + patientID + "P-merged-recal.bam"; 

	string newDIR = OutputDIR + patientID + "_MuTect/";
	testMkdir(newDIR);

	string outputFile =  newDIR + patientID + "-muTect-out.txt";
	string coverageFile = newDIR + patientID + "-muTect-coverage.txt";
	
	string analysisType = "MuTect";
	MuTect(recalNormalBAM, recalTumorBAM, outputFile, coverageFile, analysisType);

}

void MuTect(string normal_inputFile, string tumor_inputFile, string outputFile, string coverageFile , string analysisType)
{

	string command = "java "+ XmxMuTect + " -jar " + mutect + " --analysis_type " + analysisType +  " --reference_sequence " + FASTA  + " --cosmic " + COSMIC +  " --dbsnp " + DBSNP + " --input_file:normal " + normal_inputFile + "  --input_file:tumor " + tumor_inputFile + " --out " + outputFile + " --coverage_file " + coverageFile; 
	systemCall(command);

//java -Xmx8g -jar /home/abahman/Tools/mutect-src/muTect-1.1.4.jar --analysis_type MuTect --reference_sequence /home/abahman/Tools/Tools/data/hg19/ucsc.hg19.fasta --cosmic /home/abahman/Tools/Tools/data/hg19/Cosmic/Cosmic.hg19.vcf --dbsnp /home/abahman/Tools/Tools/data/hg19/dbsnp_138.hg19.vcf --input_file:normal Output/CF119C/CF119C-merged-recal.bam --input_file:tumor Output/CF119P/CF119P-merged-recal.bam --out Output/CF119-muTect-out.txt --coverage_file  Output/CF119-muTect-coverage.txt
}

string createRG(string patientID, string laneID){

	return "@RG\\tID:" + patientID + "." + laneID + "\\tSM:" + patientID + "\\tPL:" + PL; 

} 

void bwaCall(string rg, string inputFasta, string inputFastqFile1, string inputFastqFile2, string outputSAMFile){
	std::ostringstream stm ;
	stm << bwacore;
	string command = bwa + " mem -aM -t " + stm.str() + " -R \"" + rg + "\" " + inputFasta +" " + inputFastqFile1 + " " + inputFastqFile2 + " > " + outputSAMFile;
	systemCall(command);
} 

void sortSAM(string inputSAMFile, string outputBAMFileSort, string OP, string MISC){
	string command = "java "+ XmxSortSAM + " -jar " + sortsam + " I=" + inputSAMFile + " O=" +outputBAMFileSort + " SO=" + OP + " " + MISC; 
	systemCall(command);


}

void markDuplicates( string inputBAMFile, string outputBAMFileSortDUP, string metricFile, string MISC){
	string command = "java " + XmxMarkDUP + " -jar " + markdup + " I=" + inputBAMFile + " O=" + outputBAMFileSortDUP + " M=" + metricFile + " " + MISC;  
	systemCall(command);
}


void buildBAMIndex(string in_outBAMFileSortDUP, string MISC){
	string command = "java " + XmxBAMIndex  + " -jar " + buildbamindex + " INPUT=" + in_outBAMFileSortDUP + " " + MISC;
	systemCall(command);
}

void GATKIndelRealigner(string inputFasta, string inutBAMFileSortDUP, string knownIndelFile, string realignIntFile, string outputBAMFileRealigned, string MISC){
	string command = "java " + XmxRealign +  " -jar " + gatk + " -T IndelRealigner " + " -R " + inputFasta + " -I " + inutBAMFileSortDUP + " -known " + knownIndelFile + " -targetIntervals " + realignIntFile + " -o " + outputBAMFileRealigned + " " + MISC;    
	systemCall(command);
}

void GATKBaseRecalibrator(string inputFasta, string inputBAMFileRealigned, string knownVCF, string knownIndel, string realignInt, string recalTableFile, string MISC){
	string command = "java "+  XmxRecalib +" -jar " + gatk + " -T BaseRecalibrator " + " -R " + inputFasta + " -I " + inputBAMFileRealigned + " -knownSites " + knownVCF + " -knownSites " + knownIndel + " -L " + realignInt + " -o " + recalTableFile + " " + MISC;
	systemCall(command);
}

void GATKRealignerTargetCreator(string inputFasta, string inutBAMFileSortDUP, string knownIndelFile, string realignIntFile, string MISC){

	string command = "java " + XmxRealignTarget  +" -jar " + gatk + " -T RealignerTargetCreator " + " -R " + inputFasta + " -I " + inutBAMFileSortDUP + " --known " + knownIndelFile + " -o " + realignIntFile + " " + MISC;    

	systemCall(command);
}

void GATKPrintReads(string inputFasta, string BAMFileRealigned,  string recalTableFile, string recalBAM, string MISC){

	string command = "java "+XmxPrintReads + " -jar " + gatk + " -T PrintReads " + " -R " + inputFasta + " -I " + BAMFileRealigned + " -BQSR " + recalTableFile + " -o " + recalBAM + " " + MISC;    

	systemCall(command);
}
void GATKCombine(string inputFasta, string output, string recalBAMs, string MISC){

	//java -jar gatk -T PrintReads  -R fasta  -o output.bam -I L002.bam -I L002.bam -I L003.bam -I L004.bam --read_filter MappingQualityZero
	string command = "java "+XmxCombine + " -jar " + gatk + " -T PrintReads " + " -R " + inputFasta + " -o " + output + " " + recalBAMs + " --read_filter MappingQualityZero " + MISC;    

	systemCall(command);
}
