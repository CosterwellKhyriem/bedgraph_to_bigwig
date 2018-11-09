# bedgraph_to_bigwig
simple python code to convert bedGraph files to bigwig. 
The bedGraph file does not have to be sorted.

This code depends on the following modules that must be installed before using:
numpy
pyBigWig

This a simple python script can be used to convert bedgraph files to bigwig.
It requires the bedgraph file and chromosome size information.
The crhomosome size information for each organism  can be downloaded from UCSC.
Alternatively, one can also use the header information from bam files used to generate the bedgraph for retieving chromosome size infromation
The following linux command can be used to make the chromsome size infor file from bam files:


samtools view -H in.bam | grep @SQ | awk '{print $2"\t"$3}' | sed 's/SN://g' | sed 's/LN://g' > chromosomeSizeFile.txt

###################################################################################################################
                                             RUNNING
                                             
                                             
python makeBedGraphToBigWig.py --b in.bdg --c chromSize.txt --o out.bw                                             
                                             
