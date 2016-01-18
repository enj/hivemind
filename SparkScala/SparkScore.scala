/**
 * This is driver class for running cox, binomial, and gaussian algorithms.
 * @author Amir Bahmani
 *
 */

/**
 * Package object for package sparkbasics.
 * The content of this object is accessible to everything inside this package
 		 *
		 * Assumption: Genotype Matrix created based on Gene Subsets in
		 * advance!!! Read input files
		 *
		 * 1) Genotype matrix (Column-based): 
		 *    KEY:SNP ID and VALUE: PID1,Val1,PID2,Val2 ... PIDn,Valn 
		 *    Format: SNPID&PID1,Val1 PID2,Val2 ..., PIDn,Valn
		 * 
		 * 2) Pairs of Time and Event per patient; 
		 *    PID1,Time1,Event1, ..., PIDn,Timen,Eventn 
		 *    HashMap for Cox: <PID, <Time,Event>> for Gaussian
		 *    and Binomial: PID,EVENT {int, double}
		 *
		 *
		 * 3) Type score=c("cox", "binomial", "gaussian")
		 *
		 *
		 * 4) Gene Subsets GSubID SNPIDs $XYZ9 [1] "rs688" "rs469" "rs557"
		 * "rs990" "rs346" "rs962" "rs501" "rs630" "rs913" "rs32" "rs802" <GSub
		 * ID>, List of SNPs
		 *
		 * 5) Weights of SNPs - HashMap <SNPID, Weight>
		 *
		 * 6) [Optional] Number of Patients, Number of Iterations
		 * 
		 * 7) Type of Permutations: Resampling or MonteCarlo
		 *
 **/
package object SparkScore{


import org.apache.spark.SparkContext
import org.apache.spark.SparkConf

import scala.math._
import scala.collection.mutable.ArrayBuffer

var numPermutation = 0
var numPatients = 0
val DEBUG = true
val CACHE = false

// Create spark configuration object with an app name and master URL
val conf = new SparkConf() 
// Create a spark context object
val sc = new SparkContext(conf)

def main(args: Array[String]) {

		// STEP-1: read input parameters and validate them
		if (args.length < 5) {
			println("Usage: SparkSNP <Gfilename> <TimeEventFilename> <FunctionType> <GSubsetFilename> <Num of Patients>,<Num of Permutations> <SNPWeightFilename> <CovFilename>");
			System.exit(1);
		}


		val inputPathG = args(0)
		println("Gene Matrix inputPath: <file>= " + inputPathG)

		val inputPathTimeEvent = args(1)
		println("Time-Event inputPath: <file>= " + inputPathTimeEvent)

		val inputFunctionType = args(2)
		println("Input Function Type: cox, binomial , gaussian: "+ inputFunctionType)

		val inputPathGSubset = args(3)
		println("Gene Subset inputPath: <file>= " + inputPathGSubset)

		val inputPathWeight = args(4)
		println("Weight inputPath: <file>= " + inputPathWeight)

		var inputTypePermutaion = "" 
		var inputPathWG  = ""

		if (args.length >= 6) {
			val tokens = args(5).split(",")
			numPermutation = tokens(0).toInt
			numPatients = tokens(1).toInt
			println("Number of Permutations: " + numPermutation)
			println("Number of Patients: " + numPatients)

			if (args.length >= 7) {
				inputTypePermutaion = args(6) // Resampling or MonteCarlo
				println("Permutation Type =" + inputTypePermutaion)
			}

			if (args.length >= 8) {
				inputPathWG = args(7)
				println("Patient Weight inputPath: <file>= " + inputPathWG)
			}
		}

		if (inputFunctionType == "cox") {
			println("Cox")
			SparkScore.Cox.cox(inputPathG, inputPathTimeEvent, inputPathGSubset, 
		inputPathWeight, inputTypePermutaion,  inputPathWG)
		}
		else if (inputFunctionType=="binomial") {
			println("Binomia")
			SparkScore.Binomial.binomial(inputPathG, inputPathTimeEvent, inputPathGSubset, 
		inputPathWeight, inputTypePermutaion,  inputPathWG)
		}
		else if (inputFunctionType=="gaussian") {
			println("Gaussian")
			SparkScore.Gaussian.gaussian(inputPathG, inputPathTimeEvent, inputPathGSubset, 
		inputPathWeight, inputTypePermutaion,  inputPathWG)
		}
		else {
			throw new Exception("function type is undefined: inputFunctionType="+inputFunctionType);
		}
    }
  }

