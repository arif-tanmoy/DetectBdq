'''
A SIMPLE SCRIPT TO DETECT Bdq LINEAGE (4.3.1.3q1) of Salmonella Typhi
Takes VCF file as input, needs to be one-isolate-VCF (do not support multi-isolate-VCF or merged_VCF).
Test VCF file was generated using bowtie2-samtools-bcftools.

USE: python DetectBdq.py --vcf <VCF_file> --phred_cutoff <MINIMUM_PHRED_QUALITY> --output <OUTPUT_File>
'''

from argparse import (ArgumentParser, FileType)
def parse_args():
	"Parse the input arguments, use '-h' for help"
	commands = ArgumentParser(description='Detect genotype 4.3.1.3q1 lineage of Salmonella enterica serovar Typhi using mapped VCF file (against S. Typhi CT18 strain).')
	commands.add_argument('--vcf', type=str, required=True,
						help='Mapped VCF file against the S. Typhi CT18 genome (Required).')
	commands.add_argument('--phred_cutoff', type=int, required=False, default=20,
						help='Minimum phred quality score. (default 20)')
	commands.add_argument('--output', type=str, required=False, default='Bdq_detect.txt',
						help='Location and name for output file.')
	return commands.parse_args()
args = parse_args()
vcf = open(args.vcf, 'r')
output = open(args.output, 'w')

# Setup Strain ID
if "/" in str(args.vcf):
	strainID=str(args.vcf).split("/")[-1]
else:
	strainID=str(args.vcf)

## SNP loci to define genotype 4.3.1.3q1 (as described in Tanmoy et al 2018, DOI: 10.1128/mBio.02112-18.)
bdq_loci = [1253109, 2385340, 2676540, 2688285]
bdq_snp_alleles = ['G', 'G', 'T', 'T'] 
snp_found = []
snp_prop = []

for line in vcf:	# Open VCF file
	if line.startswith('#') == False:
		REFSEQ,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,RATIO = line.split('\t')
		# Calculate read_proportion
		m=INFO.split('DP4=')[1].split(';')[0].split(',')
		alt_count=int(m[2])+int(m[3])
		total_count=alt_count+int(m[1])+int(m[0])
		read_proportion= float(alt_count) / float(total_count)
		phred = float(QUAL)

		## Let's check if the strain belong to genotype 4.3.1.3q1
		if (REFSEQ== 'NC_003198.1' or REFSEQ == 'AL513383.1') and int(POS) in bdq_loci and ALT in bdq_snp_alleles and phred >= float(args.phred_cutoff):
			j=bdq_loci.index(int(POS))
			snp_found.append(bdq_loci[j])
			snp_prop.append(float(read_proportion))

snp_number=len(snp_found)
print('Number of loci for genotype 4.3.1.3q1 found: '+str(snp_number))

# Calculate median read proportion
if snp_number > 0:
	snp_prop.sort() 
	mid = len(snp_prop) // 2
	res = (snp_prop[mid] + snp_prop[~mid]) / 2
	med_read_proportion = str(round(res))
	
## Let's get the results in a file
output.write('\t'.join(
				['StrainID', 'Bdq_Status', 'Bdq_Loci_max_support\n']))
if snp_number == len(bdq_loci):
	output.write(strainID+'\t'+'4.3.1.3q1'+'\t'+med_read_proportion+'\n')
if len(bdq_loci) > snp_number > 0:
	output.write(strainID+'\t'+'Not-4.3.1.3q1(Only_'+str(snp_number)+'_SNPs_found:'+(','.join(map(str, snp_found)))+')'+'\t'+med_read_proportion+'\n')
if snp_number == 0:
	output.write(strainID+'\t'+'Not-4.3.1.3q1(No_SNPs_found)'+'\t'+'\n')

vcf.close()
output.close()