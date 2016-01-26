#include "preprocessing.h"

void createSubdirectories(){

	string outputDIR;

	string filename = DES_CSV, line, hitLine;
	char * sFilename = new char[filename.length() + 1];
	strcpy(sFilename,filename.c_str());
	vector<string> splitLine, splitHitLine;
	ifstream read(sFilename);

	while( getline(read,line) ) {
		splitLine = split(line, ',');
		string outputDIR = OutputDIR + splitLine[1] + "/";
		testMkdir(outputDIR);
	}

	read.close();	
}



int checkAllFiles(){

	string filename = DES_CSV, line;

	char * sFilename = new char[filename.length() + 1];
	std::strcpy(sFilename,filename.c_str());
	std::vector<std::string> splitLine;
	int retVal = 0; 
	ifstream read(sFilename);

	while( getline(read,line) ) {
		splitLine = split(line, ',');
		if ( checkFileExists(splitLine[3]) != 0){
			cout << splitLine[3] << " not found!" << endl;
			retVal=1;
		}
		if ( checkFileExists(splitLine[4]) != 0){
			cout << splitLine[4] << " not found!" << endl;
			retVal=1;
		}

	}

	return retVal;
}


vector<string> &split(const string &s, char delim, vector<string> &elems) {
	stringstream ss(s);
	string item;
	while (getline(ss, item, delim)) {
		elems.push_back(item);
	}
	return elems;
}


vector<string> split(const string &s, char delim) {
	vector<string> elems;
	split(s, delim, elems);
	return elems;
}


string getDirectory(const string& str)
{
	size_t found;
	found=str.find_last_of("/\\");
	return str.substr(0,found);
}

void compute (int rank, int numprocs, char pipelineType){

	string filename = DES_CSV, line, hitLine, filenamePatient = PATIENT_CSV;
	int lineNumber = 0;
	char * sFilename = new char[filename.length() + 1];
	strcpy(sFilename,filename.c_str());
	vector<string> splitLine, splitHitLine;
	int retVal = 0; 
	ifstream read(sFilename);

	if (pipelineType == 'F') // First Phase -> applies on Lanes
	{
		/*Prepration phase: read all files and put the in a file - prepare the DEC.dev file */
		while( getline(read,line) ) {

			if (numprocs  == lineNumber) // covers the case where #procs < #patients
				lineNumber = 0;

			if( lineNumber  ==  rank){
				splitLine = split(line, ',');
				//cout << "My rank is: " << rank << " Index: " << splitLine[0] <<" Patient ID: " << splitLine[1]  << " Lane ID: "<< splitLine[2] <<  endl; 
				cout << "------------------------Lane:" << splitLine[2] <<"-------------------------------" << endl;
#ifdef CXXCODE
				runPipeline(splitLine[0], splitLine[1], splitLine[2], splitLine[3], splitLine[4]);
#elif PYTHON
				systemCall(pipeline.py splitLine[0] splitLine[1] splitLine[2] splitLine[3] splitLine[4]);
#endif

			}

			lineNumber++;

		}

		read.close();	
		MPI_Barrier(MPI_COMM_WORLD);
	}
	else if (pipelineType == 'S') // Second Phase creates merge files
	{

		ifstream read2(sFilename);
		string merge="";
		while( getline(read2,line) ) {
			splitLine = split(line, ',');
			//cout << "rank: " << rank << " size: " << splitLine.size() << endl;
			if (atoi(splitLine[5].c_str()) % numprocs == rank) // covers the case where #procs < #patients
			{
				hitLine = line; 
				merge = merge + splitLine[2] + ";"; //L001;L002;L003;L004;
			}
			else if(merge!=""){
				splitHitLine = split(hitLine, ',');
				cout << "------------------------Merge:" << merge <<"-------------------------------" << " rank: " << rank <<endl;
				string targetDir = getDirectory(splitHitLine[3]); 
				runPipeline(splitHitLine[0], splitHitLine[1], split(merge, ';'), targetDir);
				merge = "";
			}
		}
		if(merge!=""){
			splitHitLine = split(hitLine, ',');
			cout << "------------------------Merge:" << merge <<"-------------------------------" << " rank: "<< rank << endl;
			string targetDir = getDirectory(splitHitLine[3]); 
			runPipeline(splitHitLine[0], splitHitLine[1], split(merge, ';'), targetDir);
			merge = "";


		}

		read2.close();
	}
	else if (pipelineType == 'T') // Applies MuTect
	{
		cout << filenamePatient<< endl;
		char * pFilename = new char[filenamePatient.length() + 1];
		
		strcpy(pFilename,filenamePatient.c_str());
		ifstream read(pFilename);
		while(getline(read,line) ) {
			splitLine = split(line, ',');
			//cout << "rank: " << rank << " size: " << splitLine.size() << endl;
			if ( lineNumber % numprocs == rank) // covers the case where #procs < #patients
			{
				cout << "------------------------MuTect: " <<  splitLine[0] <<"-------------------------------" << " rank: " << rank <<endl;
				runPipeline( splitLine[0]);
			
			}
			lineNumber++;
		}


		read.close();
	}

}	

int main(int argc, char** argv){

	int rank, numprocs;
	FILE *f1;
	int i;

	MPI_Init(&argc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);

	if(numprocs < 2)
	{
		cerr << "Number of processses must be larger than two!" << endl;
		MPI_Finalize();
		return 0;
	}

	if (argc<2){
		cout << "Not enough or invalid arguments, please try again.\n";
		MPI_Finalize();
		return 0;
	}

	char pipelineType = *argv[1];

	if (pipelineType == 'F') // Call Lane Phase
	{
		/* Chcek input files */
		int status =0; 
		if (rank == 0){
			if (checkAllFiles() == 1){
				cerr << "Some input files are missing!"<< endl;
				status =1;
			}

			createSubdirectories();
		}

		MPI_Bcast(&status, 1, MPI_INT, 0, MPI_COMM_WORLD);

		if (status == 1){
			MPI_Finalize();
			return 0;
		}

		MPI_Barrier(MPI_COMM_WORLD);
	}


	struct timeval tim;
	gettimeofday(&tim, NULL);
	double t1=tim.tv_sec+(tim.tv_usec/1000000.0);

	compute(rank, numprocs, pipelineType);

	gettimeofday(&tim, NULL);
	double t2=tim.tv_sec+(tim.tv_usec/1000000.0);
	printf("Compute Time: %.6lf seconds elapsed\n", t2-t1);


	MPI_Finalize();

	return 0;
}
