# DetectBdq

This simple script determines whether a *Salmonella* Typhi genome belongs to lineage Bdq, first described in: [*Salmonella enterica* Serovar Typhi in Bangladesh: Exploration of Genomic Diversity and Antimicrobial Resistance, Tanmoy et al, 2018, mBio](http://mbio.asm.org/content/9/6/e02112-18).
This lineage is a part of lineage Bd (Later renamed as genotype 4.3.1.3) which was also first described in the same article. Lineage Bdq was later described as **4.3.1.3q1** in here: [CRISPR-Cas Diversity in Clinical *Salmonella enterica* Serovar Typhi Isolates from South Asian Countries, Tanmoy et al, 2020, Genes](https://www.mdpi.com/2073-4425/11/11/1365).

## Requirements:
The script filters through the VCF file, mapped against *Salmonella* Typhi CT18 (accession: [NC_003198.1](https://www.ncbi.nlm.nih.gov/nuccore/NC_003198) or, [AL513382.1](https://www.ncbi.nlm.nih.gov/nuccore/AL513382)).
This VCF file needs to be based on a single genome. This script cannot process a merged VCF or a VCF based on multiple genomes.

## Usage
```
python DetectBdq.py --vcf <VCF_file> --phred_cutoff <Minimum_Phred_Score> --output <Output_File>
```

## Options
### Required Options
```
--vcf      VCF file of single isolate, mapped against Salmonella Typhi CT18.
```

### Specific options
```
--phred_cutoff      Minimum Phred Score (default 20).
--output            Output file (default: Bdq_detect.txt).
```

## Output
The script calculates the proportion of reads for each of the SNP positions. As the genotype 4.3.1.3q1 relies on four different SNPs (based on this [article](http://https://mbio.asm.org/content/9/6/e02112-18)), this script also calculates the median read_proportion value.
### Output format
```
SampleID <tab> 4.3.1.3q1_or_not <tab> Median_read_proportion
```
