import os
from os import path
import argparse
import math
from services.logging_service import get_logger
from services.data_service import divide, merge

INPUT_DIR = './data/input'
OUTPUT_DIR = './data/output'
TMP_DIR = './data/tmp'
DEFAULT_MEMORY_LIMIT = 20
FD_LIMIT = 100
LOGGER = get_logger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("The application sorts very large files.")
    parser.add_argument('filename', type=str, help=f'Define file name. This file should be places in {INPUT_DIR}.')
    parser.add_argument('--mem_limit', type=int, default=DEFAULT_MEMORY_LIMIT,
                        help=f'Memory limit in megabytes (only data, exclude app). Default: {DEFAULT_MEMORY_LIMIT}Mb.')

    args = parser.parse_args()

    input_file = path.join(INPUT_DIR, args.filename)
    if not path.isfile(input_file):
        raise ValueError("Invalid a file name.")

    if args.mem_limit <= 0:
        raise ValueError("The size of the memory limit should be more than 0.")

    input_file_stat = os.stat(input_file)
    file_size_in_mb = round(input_file_stat.st_size / (1024 * 1024), 2)

    LOGGER.info(f"""Job params: 
    - Memory limit {args.mem_limit}Mb; 
    - Memory for single partition {args.mem_limit}Mb; 
    - Path to the file: {input_file};
    - Size of the file: {file_size_in_mb}Mb;
    - Raw size of the file: {input_file_stat.st_size} bytes;
    - Approximately number of partitions: {math.ceil(file_size_in_mb / args.mem_limit)};
    """)

    divide(input_file, TMP_DIR, args.mem_limit)

    merge(TMP_DIR, OUTPUT_DIR, args.filename)
