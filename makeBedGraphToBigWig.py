"""This a simple python script can be used to convert bedgraph files to bigwig.
   It requires the bedgraph file and chromosome size information.
   The chromosome size information for each organism  can be downloaded from UCSC.
   Alternatively, one can also use the header information from bam files used to generate the bedgraph for retieving chromosome size infromation"""
import sys
import numpy as np
import pyBigWig as bw
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--b',dest='input_bedgraph',required=True, help='bedgraph file ; required')
parser.add_argument('--c',dest='chromosome_sizes',help='chromsome size information file')
parser.add_argument('--o',dest='outputFileName',required=True, help='Name of the output file; required')

if len(sys.argv)==1:
	parser.print_help(sys.stderr)
	sys.exit(1)
information = parser.parse_args()

bedgraphFile = str(information.input_bedgraph)
chromosomeSize = str(information.chromosome_sizes)
outputFileName = str(information.outputFileName)


def sorted_nicely( l ):
	""" Sorts the given iterable in the way that is expected.
	https://arcpy.wordpress.com/2012/05/11/sorting-alphanumeric-strings-in-python/
	Required arguments:
	l -- The iterable to be sorted."""

	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key = alphanum_key)
	

chrom = []
ends = []
starts = []
counts = []

print "\n\n\t\tReading the chromosome information file...\n"
with open(chromosomeSize) as file:
	chromosomesRef = {}
	for line in file:
		row=line.split('\t')
		chromosomesRef[str(row[0])] = int(row[1])

print "\t\tReading the bedgraph file....\n"
with open(bedgraphFile) as file:
	for line in file:
		row=line.split('\t')
		chrom.append(str(row[0]))
		starts.append(int(row[1]))
		ends.append(int(row[2]))
		counts.append(float(row[3]))

chrom = np.asarray(chrom)
starts = np.asarray(starts,dtype=np.int64)
ends = np.asarray(ends,dtype=np.int64)
counts = np.asarray(counts)


headerArray = []
for chromosome in sorted_nicely(chromosomesRef.keys()):
	headerArray.append((chromosome,chromosomesRef[chromosome]))

print "\t\tMaking the bigwig file....\n"
bwFile=bw.open(sys.argv[3], "w")
bwFile.addHeader(headerArray, maxZooms=10)
for chromosome in sorted_nicely(chromosomesRef.keys()):
	bwFile.addEntries(chrom[np.where(chrom==chromosome)],starts[np.where(chrom==chromosome)],ends=ends[np.where(chrom==chromosome)],values=counts[np.where(chrom==chromosome)])
bwFile.close()
print "\t\tAll done\n"
