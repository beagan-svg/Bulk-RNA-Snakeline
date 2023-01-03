# PyPackages to import
import os
import re
import sys
import argparse

# Arg_parser
def getArgs():
    parser = argparse.ArgumentParser(
        description='Optional arguments: -s', usage='python3 final_deduper.py -s <sample_list.txt>'
    )

    parser.add_argument(
        '-s', '-sample', help='Input list of sample names', required=False
    )

    return parser.parse_args()

# Make Directories for FASTQ files
os.system('mkdir -p Pipeline')
os.system('mkdir -p Pipeline/Fastq')
os.system('mkdir -p Pipeline/Fastq/Raw')
os.system('mkdir -p Pipeline/Fastq/CutAdapt')

# Make Directories for QC files
os.system('mkdir -p Pipeline/QC')
os.system('mkdir -p Pipeline/QC/Raw')
os.system('mkdir -p Pipeline/QC/CutAdapt')

# Make Directories for STAR
os.system('mkdir -p Pipeline/STAR')
os.system('mkdir -p Pipeline/STAR/genome')

# Make Directories for StringTie
os.system('mkdir -p Pipeline/StringTie')

# Samples files must follow <sample_name>R1_<digits>.fastq.gz
get_fastq = re.compile('(.*R1_\d*fastq.gz$)|(.*R2_\d*fastq.gz$)')

# Search for fastq files
r1_list = list()
r2_list = list()
current_dir = os.getcwd()
for root, dirs, files in os.walk(current_dir):
    for file in files:
        res = re.match(get_fastq, file)
        if res:
            if res.group(1):
                r1_list.append(os.path.join(root, file))
            if res.group(2):
                r2_list.append(os.path.join(root, file))

# Move Fastq files to raw directory
for fastq_file_path in r1_list:
    if 'Pipeline/Fastq/Raw' not in fastq_file_path:
        os.system('mv {} Pipeline/Fastq/Raw'.format(fastq_file_path))

for fastq_file_path in r2_list:
    if 'Pipeline/Fastq/Raw' not in fastq_file_path:
        os.system('mv {} Pipeline/Fastq/Raw'.format(fastq_file_path))

# --------------------------------------
# Input/Outputs
args = getArgs()
fastq_name_list = list()

# If sample_list.txt is supplied
if args.s:
    sample_txt_open = open(args.s, 'r')   
    for sample_name in sample_txt_open:
        fastq_name_list.append(sample_name.rstrip())
else:
    # Store all available raw fastq file names into a list
    fastq_files_list = os.listdir('Pipeline/Fastq/Raw')
    for fastq_files in sorted(fastq_files_list):
        if 'R1' in fastq_files:
            suffix_fastq_file = fastq_files.replace("_R1_001.fastq.gz", "")
            fastq_name_list.append(suffix_fastq_file)
        else:
            suffix_fastq_file = fastq_files.replace("_R2_001.fastq.gz", "")
            fastq_name_list.append(suffix_fastq_file)

# Clear existing input and output names for the samples
fappen = open('configs/config.yml', 'r')
lines = fappen.readlines()
io_index = len(lines)

if '# Append\n' in lines:
    io_index = lines.index('# Append\n')
    print(io_index)
fappen.close()

fappen = open('configs/config.yml', 'w')
filtered_lines = lines[0: io_index+1]
for line in filtered_lines:
    fappen.write(line)
fappen.close()

# Sort and remove duplicates of fastq names
sorted_fastq = sorted([*set(fastq_name_list)])

# Append config yml file by adding input names for the samples key
original_stdout = sys.stdout
with open('configs/config.yml', 'a') as f:
    sys.stdout = f
    print(' {}'.format(sorted_fastq))
    sys.stdout = original_stdout





