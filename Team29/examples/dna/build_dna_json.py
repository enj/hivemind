#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dump

output_json = "test.json"
wd = "/home/temp1037/dna"

#Reference Files
fasta = "/home/temp1037/Duke/Tools/data/hg19/ucsc.hg19.fasta"
knownindel = "/home/temp1037/Duke/Tools/data/hg19/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf"
knownvcf = "/home/temp1037/Duke/Tools/data/hg19/NA12878.HiSeq.WGS.bwa.cleaned.raw.subset.hg19.sites.vcf"
capture = "/home/temp1037/Duke/Tools/data/S04380219_Covered.bed"
cosmic = "/home/temp1037/Duke/Tools/data/hg19/Cosmic/Cosmic.hg19.vcf"
dbsnp = "/home/temp1037/Duke/Tools/data/hg19/dbsnp_138.hg19.vcf"

#Programs
bwa = "/home/temp1037/Duke/Tools/bwa.kit/bwa"
bwa_cores = "16"
sortsam = "/home/temp1037/Duke/Tools/picard-tools-1.119/SortSam.jar"
markdup = "/home/temp1037/Duke/Tools/picard-tools-1.119/MarkDuplicates.jar"
buildbam = "/home/temp1037/Duke/Tools/picard-tools-1.119/BuildBamIndex.jar"
gatk = "/home/temp1037/Duke/Tools/GenomeAnalysisTK.jar"
mutect = "/home/temp1037/Duke/Tools/MuTect/muTect-1.1.4.jar"
merge_lanes = "python /home/temp1037/bin/merge_lanes.py"
java6 = "/usr/java/jdk1.6.0_16/bin/java"

#Lane
patient_path = "data/$$patient$$/"
f1 = "_R1.fastq.gz"
f2 = "_R2.fastq.gz"
bwa_rg = "'@RG\\tID:$$patient$$P###.L###\\tSM:$$patient$$P###\\tPL:ILLUMINA'"

#Files
samfile = ".sam"
bamfilesort = "-sort.bam"
bamfilesortdup = "-sort-dup.bam"
metricfile = "-dup-metrics.txt"
bamfilerealigned = "-sort-dup-realign.bam"
recaltable = "-recal-table.txt"
realignint = "-realign.intervals"
recalbam = "-recal.bam"
mergedbam = ".bam"
mergeddup = "-dup.bam"
mutectfile = "muTect-out.txt"
mutectcover = "muTect-coverage.txt"

#Not knowing if MuTect intervals are usually used or not, or if it's by patient:
intervals = "chr17:1-7577200"
#intervals = "'$$intervals$$'"
#intervals = None

#pipeline = []
pipelines = {}

for t in ["C", "P"]:
    for lane in ["L001", "L002", "L003", "L004", "merged"]:
        pipelines["{}{}".format(lane, t)] = []
        pipeline = pipelines["{}{}".format(lane, t)]
        bam = bamfilesort
        dup = bamfilesortdup
        if lane is not "merged":
            stage_align = {
                "_uid": "align_{}{}".format(lane, t),
                "wd": wd,
                "shell": "true",
                "exe": bwa,
                "args": [
                    "mem",
                    "-aM",
                    "-t",
                    bwa_cores,
                    "-R",
                    bwa_rg.replace("L###", lane).replace("P###", t),
                    fasta,
                    "{}{}/{}{}".format(patient_path, t, lane, f1),
                    "{}{}/{}{}".format(patient_path, t, lane, f2),
                    ">",
                    "{}{}/{}{}".format(patient_path, t, lane, samfile)
                ]
            }
            if lane is "L003" or lane is "L004":
                stage_align["skip"] = "$$skip_{}$$".format(lane)
            pipeline.append(stage_align)

            stage_sort = {
                "_uid": "sort_{}{}".format(lane, t),
                "_requires": ["align_{}{}".format(lane, t)],
                "wd": wd,
                "exe": "java",
                "args": [
                    "-jar",
                    sortsam,
                    "I={}{}/{}{}".format(patient_path, t, lane, samfile),
                    "O={}{}/{}{}".format(patient_path, t, lane, bam),
                    "SO=coordinate"
                ]
            }
            if lane is "L003" or lane is "L004":
                stage_sort["skip"] = "$$skip_{}$$".format(lane)
            pipeline.append(stage_sort)
        else:
            bam = mergedbam
            dup = mergeddup
            stage_merge = {
                "_uid": "mergeLanes_{}".format(t),
                "_requires": ["recalBAM_L001{}".format(t), "recalBAM_L002{}".format(t), "recalBAM_L003{}".format(t), "recalBAM_L004{}".format(t)],
                "wd": wd,
                "exe": merge_lanes,
                "shell": "true",
                "args": [
                    "-e",
                    "'java -jar {}'".format(gatk),
                    "-T",
                    "PrintReads",
                    "-R",
                    fasta,
                    "-I",
                    "{}{}/L001{}".format(patient_path, t, recalbam),
                    "-I",
                    "{}{}/L002{}".format(patient_path, t, recalbam),
                    "-I",
                    "{}{}/L003{}".format(patient_path, t, recalbam),
                    "-I",
                    "{}{}/L004{}".format(patient_path, t, recalbam),
                    "--read_filter",
                    "MappingQualityZero",
                    "-o",
                    "{}{}/{}{}".format(patient_path, t, lane, mergedbam)
                ]
            }
            pipeline.append(stage_merge)

        stage_markdup = {
            "_uid": "markDup_{}{}".format(lane, t),
            "_requires": ["sort_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                markdup,
                "I={}{}/{}{}".format(patient_path, t, lane, bam),
                "O={}{}/{}{}".format(patient_path, t, lane, dup),
                "M={}{}/{}{}".format(patient_path, t, lane, metricfile)
            ]
        }
        if lane is "merged":
            stage_markdup["_requires"] = ["mergeLanes_{}".format(t)]
        if lane is "L003" or lane is "L004":
                stage_markdup["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_markdup)

        stage_indexbam = {
            "_uid": "indexBAM_{}{}".format(lane, t),
            "_requires": ["markDup_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                buildbam,
                "INPUT={}{}/{}{}".format(patient_path, t, lane, dup),
                "OUTPUT={}{}/{}{}.bai".format(patient_path, t, lane, dup)
            ]
        }
        if lane is "L003" or lane is "L004":
                stage_indexbam["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_indexbam)

        stage_create_targets = {
            "_uid": "createTargets_{}{}".format(lane, t),
            "_requires": ["indexBAM_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                gatk,
                "-T",
                "RealignerTargetCreator",
                "-R",
                fasta,
                "-I",
                "{}{}/{}{}".format(patient_path, t, lane, dup),
                "--known",
                knownindel,
                "-o",
                "{}{}/{}{}".format(patient_path, t, lane, realignint)
            ]
        }
        if lane is "L003" or lane is "L004":
                stage_create_targets["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_create_targets)

        stage_reallign = {
            "_uid": "reallign_{}{}".format(lane, t),
            "_requires": ["createTargets_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                gatk,
                "-T",
                "IndelRealigner",
                "-R",
                fasta,
                "-I",
                "{}{}/{}{}".format(patient_path, t, lane, dup),
                "-known",
                knownindel,
                "-targetIntervals",
                "{}{}/{}{}".format(patient_path, t, lane, realignint),
                "-o",
                "{}{}/{}{}".format(patient_path, t, lane, bamfilerealigned),
                "--filter_bases_not_stored"
            ]
        }
        if lane is "L003" or lane is "L004":
                stage_reallign["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_reallign)

        stage_recal = {
            "_uid": "recal_{}{}".format(lane, t),
            "_requires": ["reallign_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                gatk,
                "-T",
                "BaseRecalibrator",
                "-R",
                fasta,
                "-I",
                "{}{}/{}{}".format(patient_path, t, lane, bamfilerealigned),
                "-knownSites",
                knownvcf,
                "-knownSites",
                knownindel,
                "-L",
                capture,
                "-o",
                "{}{}/{}{}".format(patient_path, t, lane, recaltable)
            ]
        }
        if lane is "L003" or lane is "L004":
                stage_recal["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_recal)

        stage_recalbam = {
            "_uid": "recalBAM_{}{}".format(lane, t),
            "_requires": ["recal_{}{}".format(lane, t)],
            "wd": wd,
            "exe": "java",
            "args": [
                "-jar",
                gatk,
                "-T",
                "PrintReads",
                "-R",
                fasta,
                "-I",
                "{}{}/{}{}".format(patient_path, t, lane, bamfilerealigned),
                "-BQSR",
                "{}{}/{}{}".format(patient_path, t, lane, recaltable),
                "-o",
                "{}{}/{}{}".format(patient_path, t, lane, recalbam)
            ]
        }
        if lane is "L003" or lane is "L004":
                stage_recalbam["skip"] = "$$skip_{}$$".format(lane)
        pipeline.append(stage_recalbam)

stage_mutect = {
    "_uid": "mutect",
    "_requires": ["recalBAM_mergedP", "recalBAM_mergedC"],
    "wd": wd,
    "exe": java6,
    "args": [
        "-Xmx8g",
        "-jar",
        mutect,
        "-T",
        "MuTect",
        "-R",
        fasta,
        "-cosmic",
        cosmic,
        "-dbsnp",
        dbsnp,
        "--intervals",
        intervals,
        "--input_file:normal",
        "{}{}/{}{}".format(patient_path, "C", "merged", recalbam),
        "--input_file:tumor",
        "{}{}/{}{}".format(patient_path, "P", "merged", recalbam),
        "-o",
        "{}{}".format(patient_path, mutectfile),
        "-cov",
        "{}{}".format(patient_path, mutectcover),
    ]
}
if intervals is None:
    stage_mutect["args"].remove("--intervals")
    stage_mutect["args"].remove(None)
pipelines["mutect"] = []
pipelines["mutect"].append(stage_mutect)

for k, p in pipelines.iteritems():
    with open(k + ".json", 'w') as outfile:
        dump(p, outfile, sort_keys=True, indent=4)
