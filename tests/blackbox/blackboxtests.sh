#!/bin/sh
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

#Command to run sha sum 256
SHA='sha256sum'
#SHA='shasum -a 256'

#Linear
printf "Running test: Linear - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j linear/linear.json -c linear/linear.csv 2>&1)"
if [ "${result}" == "" ] && \
    [ "$(${SHA} linear/mo5.txt)" == "08248741d577ec6d0292ab0658b3cc42ff6a91ac25c4e390e44dde63c9b51a3b  linear/mo5.txt" ] && \
    [ "$(${SHA} linear/sarah5.txt)" == "54d99880e91909c8b46207b12b43211a89246bc890efb4be41fcb45aaac41219  linear/sarah5.txt" ] && \
    [ "$(${SHA} linear/hussein5.txt)" == "cec32d2bb5c9e78fe201fb93ebfc45d7c11d7e63c764b05ef39c10a7b33f0965  linear/hussein5.txt" ]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#DAG
printf "Running test: DAG - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j dag/dag.json -c dag/dag.csv 2>&1)"
if [ "${result}" == "" ] && \
    [ "$(${SHA} dag/sarah5_1.txt)" == "a4a15ede33b9399e8238035f2204884906a79735f4530caf206099023167bb9a  dag/sarah5_1.txt" ] && \
    [ "$(${SHA} dag/sarah5_2.txt)" == "294bbafde8905dbad648515f7aef2cc89d97d32b1bba9141bffc120e1a6ad524  dag/sarah5_2.txt" ] && \
    [ "$(${SHA} dag/sarah5_3.txt)" == "46e1803418e58a6e8bf799b66ff63b8e4a5c817ab5f2a9de21f4bd95fffdb538  dag/sarah5_3.txt" ]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#Disconnected
printf "Running test: Disconnected - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j disconnected/disconnected.json -c disconnected/disconnected.csv 2>&1)"
if [ "${result}" == "" ] && \
    [ "$(${SHA} disconnected/sarah_A2.txt)" == "2f92511275182c337091d21eaf36159bea1c39d08b321da3fa62dd9aa3378298  disconnected/sarah_A2.txt" ] && \
    [ "$(${SHA} disconnected/sarah_B2.txt)" == "6938ce33ab4539f583aea1151b63a7c9a86f13b3774e8256a25243d37b6c59a7  disconnected/sarah_B2.txt" ] && \
    [ "$(${SHA} disconnected/sarah_C2.txt)" == "5fe9fb8b9fee7767697401c9617ccee430a9aeddbd25d93364afeab5a68bffa6  disconnected/sarah_C2.txt" ]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorCycle
printf "Running test: ErrorCycle - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j cycle/cycle.json -c cycle/cycle.csv 2>&1)"
if [[ "${result}" == *"ValueError: Pipeline contains a cycle"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorDuplicateNode
printf "Running test: ErrorDuplicateNode - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j duplicate/duplicate.json -c duplicate/duplicate.csv 2>&1)"
if [[ "${result}" == *"ValueError: Pipeline contains duplicate Task"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorMissingRequired
printf "Running test: ErrorMissingRequired - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j missing_req/missing_req.json -c missing_req/missing_req.csv 2>&1)"
if [[ "${result}" == *"KeyError: 'Unknown UID A4_4 set as requirement for A5_3'"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorBadJSON
printf "Running test: ErrorBadJSON - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j bad_json/bad_json.json -c bad_json/bad_json.csv 2>&1)"
if [[ "${result}" == *"ValueError: Expecting , delimiter"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorBadCSV
printf "Running test: ErrorBadCSV - "
result="$(mpirun -n 4 python -O ../../examples/main.py -j bad_csv/bad_csv.json -c bad_csv/bad_csv.csv 2>&1)"
if [[ "${result}" == *"ValueError: Not all \$\$ variables replaced"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi

#ErrorNoArgs
printf "Running test: ErrorNoArgs - "
result="$(mpirun -n 4 python -O ../../examples/main.py 2>&1)"
if [[ "${result}" == "usage: main.py"* ]]; then
    printf "${GREEN}Pass${NC}\n"
else
    printf "${RED}Fail${NC}\n"
fi


### Anything below this will take significant time - even the "small" ones

#SmallKSRT
#qsub -l nodes=20:ppn=4 mpirun -n 80 python -O main.py -j ksrt.json -c ksrt_small.csv


#SmallDNA
#qsub -l nodes=20:ppn=4 mpirun -n 80 python -O main.py -j dna.json -c dna_small.csv


#FullKSRT
#qsub -l nodes=64:ppn=8 mpirun -n 512 python -O main.py -j ksrt.json -c ksrt_full.csv


#FullDNA
#qsub -l nodes=64:ppn=8 mpirun -n 512 python -O main.py -j dna.json -c dna_full.csv