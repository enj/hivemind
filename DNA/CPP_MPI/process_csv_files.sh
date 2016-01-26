#!/bin/bash
rm des.csv  global.csv  list_csv_files patient.csv

find  data/ -iname '*.csv' > list_csv_files
counter=0
for line in $(cat list_csv_files); do
    for line2 in $(cat "$line" | tail -n+2); do 
     echo `dirname $line`','$line2','$counter >> global.csv
    done
    counter=$((counter+1))
done



for line in $(cat global.csv); do
     #$DIR,C43AKACXX,1,CF55C,human,AAAGCA,A016,N,SureSelectExomePlus,JS,Duke
     var=$(echo $line | awk -F"," '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}')
     set -- $var     
#CGATGT,CF33C,L002,/data1/DCI/studydata/Patz/Plasma/140702_SN922_0112_AC4308ACXX/Sample_CF33C/CF33C_CGATGT_L002_R1_001.fastq.gz,/data1/DCI/studydata/Patz/Plasma/140702_SN922_0112_AC4308ACXX/Sample_CF33C/CF33C_CGATGT_L002_R2_001.fastq.gz,Counter
     echo $6','$4',L00'$3','$1'/'$4'_'$6'_L00'$3'_R1_001.fastq.gz'','$1'/'$4'_'$6'_L00'$3'_R2_001.fastq.gz,'${12} >> des.csv
done

oldpatient="NA";

for line in $(cat global.csv); do
     #$DIR,C43AKACXX,1,CF55C,human,AAAGCA,A016,N,SureSelectExomePlus,JS,Duke
     var=$(echo $line | awk -F"," '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}')
     set -- $var     
     current=$4
     current="${current%?}"
     if [ "$current" != "$old_patient" ]
	then
	    echo $current >> patient.txt
	    old_patient=$current
     fi
done

sort -u patient.txt > patient.csv
rm patient.txt
