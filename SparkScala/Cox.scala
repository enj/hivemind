package  SparkScore

import org.apache.spark.rdd._
import collection.mutable._
import scala.io._
import scala.math._
import scala.util.Random
/*
import sys.process._
val result = "ls -al"
println(result)
*/

object Cox extends App {	

	def calculateScoreStatistics(GSubMap:HashMap[String,Array[String]], 
		SUM_U_Map:scala.collection.Map[String, Double]): 
	HashMap[String, Double]={
		var GScoreMap = new HashMap[String, Double]()
		GSubMap.foreach( (ee) => {
			val SNPList = ee._2
			var score = 0.0	
			SNPList.foreach( (t) => {
					score += SUM_U_Map.get(t).get
			})
			GScoreMap += (ee._1 -> score)
			
		})
		return GScoreMap
	}


	def cox (inputPathG: String, inputPathTimeEvent: String, inputPathGSubset:String, 
		inputPathWeight:String, inputTypePermutaion:String,  inputPathWG:String){
	 
	 // STEP-1: Read Genotype Matrix : input record format: SID&PID1,Val1
	 // PID2,Val2 ... PIDn,Valn
	 val GMlines: RDD[String] = sc.textFile(inputPathG);

	 // STEP-2: Read Gene Sets
     // STEP-3: Create a set of all SNPs in geneSets
	 val GSubMap = new HashMap[String,Array[String]]()
	 val AllSNPs = new HashMap[String, Boolean]()

     scala.io.Source.fromFile(inputPathGSubset).getLines.foreach(line => {
      	line.split(",") match {
        case Array(j,t) => {
          val gensetID = j.trim
          val snpIDs = t.split(" ")
          GSubMap += (gensetID -> snpIDs)
          snpIDs.foreach ( elem => {
          	val t= (elem, true)
          	AllSNPs += t
          	})
        }
        case _ => /* Handle error? */
      }
     })

     if(DEBUG){	
		 GSubMap foreach ( (t) => println (t._1 + "-->" + t._2))
		 AllSNPs foreach ( (t) => println (t._1 + "-->" + t._2))
	 }
	
	 // STEP-4: PairedRDD for Genotype Matrix
	 val GMPairs = GMlines.map(line => (line.split("&")(0), line.split("&")(1)))

	 // STEP-5: PairedRDD for SNP Weights
	 val SNPWeightPairs = sc.textFile(inputPathWeight).map(line => (line.split(" ")(0), 
	 	math.pow(line.split(" ")(1).toDouble,2)))


     if(DEBUG){	
		 SNPWeightPairs foreach ( (t) => println (t._1 + "-->" + t._2))
	 }

	 // STEP-6:Score Statistics
	 println("<==============Score Statistics: COX=============>");
	 // STEP-1: Pairs of <PID, <Time, Event>>
	 val PatientMapHashMap = new scala.collection.mutable.HashMap[Int, (Double, Int)]()
	 scala.io.Source.fromFile(inputPathTimeEvent).getLines.foreach(line => {
	   		val values = line.split(",")
	   		val k = values(0).toInt
	   		val v1= values(1).toDouble
	   		val v2= values(2).toInt
	   		val Tupletmp = new Tuple2(v1,v2)
	   		PatientMapHashMap.put(k, Tupletmp)
	     })

     if(DEBUG){	
		 PatientMapHashMap foreach ( (t) => println (t._1 + "--> (" + t._2._1 + ", " + t._2._2 +")"))
	 }

	 // STEP-2: Generate U[i, t] matrix
	 //JavaPairRDD<String, List<Tuple2<Integer, Double>>> U0 = generateMatrix(GMPairs, map_COX);
	 val U0 = GMPairs.map(t => {
	 	val snpID = t._1
	 	val PIDandValues = t._2.split(" ")
	 	val HashMapPIDandValues = new scala.collection.mutable.HashMap[Int, Double]()
 		var SNP_COX_Elem = scala.collection.mutable.MutableList[Tuple2[Int, Double]]()

		PIDandValues foreach ( (t2) => { 
				val tem = t2.split(",")
				val PID = tem(0).toInt
				val Gij = tem(1).toDouble	
				HashMapPIDandValues += (PID->Gij)
			})

		HashMapPIDandValues foreach ((t3) => {
				val PID = t3._1
				val Gij = t3._2

				val Yi = PatientMapHashMap.get(PID).get._1
				val Delta_i = PatientMapHashMap.get(PID).get._2
				var a_ji =0.0  
				var b_i  =0

				PatientMapHashMap foreach ( (t2) => {
					if (Yi <= t2._2._1) {
							a_ji = a_ji + HashMapPIDandValues.get(t2._1).get
							b_i = b_i + 1
						}
					})
				val coxVal = Delta_i * (Gij - (a_ji/b_i));
				val Tupletmp = new Tuple2[Int, Double] (PID, coxVal)
				SNP_COX_Elem += Tupletmp
			})

		 (snpID->SNP_COX_Elem)

	 	})

     if(DEBUG){	
		 U0.collect.foreach ( (t) => println (t._1 + "--> (" + t._2 + ")"))
	 }

	 // Cache U0 for MonteCarlo Execution
	 if (numPermutation > 0)
	 	if (inputTypePermutaion.equals("MonteCarlo") && CACHE) {
	 		println("Cached U matrix!")
	 		U0.cache()
	 	}

		// STEP-6: Calculate Sigma of U[i, j] per each SNP <SNP_ID,
		// cox_value>
		val sumU0 = new PairRDDFunctions(U0.map (t => {
			val snpID = t._1
			var SNP_COX_Elem =t._2 // scala.collection.mutable.MutableList[Tuple2[Int, Double]]()	
			var sum =0.0
			SNP_COX_Elem.foreach( (e) => sum += e._2)
			(snpID -> sum)
		})) 

 	 // STEP 6: Multiply SNP by their Weights
	 val joinOuterSigma = sumU0.join(SNPWeightPairs) 
 	 //JavaPairRDD<String, Tuple2<Double, Double>> joinOuterSigma = sumU0.join(SNPWeightPairs); // squareU0
	 val outerSigma = new PairRDDFunctions( joinOuterSigma.map(s => ( s._1, (s._2._1 * s._2._1) * s._2._2 )))	

     if(DEBUG){	
		 outerSigma.collectAsMap.foreach ( (t) => println (t._1 + "--> (" + t._2 + ")"))
	 }

	 // STEP-6-1: Calculate S0 per each GeneSet
	 val SUM_U_Map = outerSigma.collectAsMap()

	 // STEP-6-2:
	 var Score0Map = new scala.collection.mutable.HashMap[String,Double] ()
	 Score0Map = calculateScoreStatistics(GSubMap, SUM_U_Map)


	}
}
