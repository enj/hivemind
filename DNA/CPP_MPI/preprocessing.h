#include <time.h>
#include <mpi.h>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include "pipeline.h"
using namespace std;

const int NUM_PATIENT = 2; 
const int NUM_LANE = 8;

//int checkFileExists(string filename);
int  checkAllFiles();
vector<string> &split(const string &s, char delim, vector<string> &elems);
vector<string> split(const string &s, char delim);
string getDirectory(const string& str);
void createSubdirectories();
