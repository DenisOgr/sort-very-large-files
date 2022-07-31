import os
import sys
import glob
from os import path

from services.logging_service import get_logger
from typing import Union

LOGGER = get_logger()
BATCH_SIZE_FOR_FLUSH = 10000


class DataProvider:
    def __init__(self, fd, cur_value):
        self.fd = fd
        self.cur_value = cur_value


def divide(input_file, tmp_dir, mem_limit_in_mb):
    """
    Read data from the input file.
    Store to temporary list.
    The size of list should be less than the limit memory (mem_limit_in_mb).
    Sort list into the memory (space = 1)
    Write to file (disc). Each list to separate file in tmp_dir directory.

    Args:
        input_file: Required. Path to the input file.
        tmp_dir: Required. Path to the temporary directory. For
        mem_limit_in_mb: Required. Size of the RAM memory. The internal data structure should be less than this value.

    """
    num = -1
    end_file = False

    with open(input_file, 'r') as in_f:
        while not end_file:
            result = []
            num += 1
            while sys.getsizeof(result) < mem_limit_in_mb * 1024 * 1024:
                number = in_f.readline()
                if not number:
                    end_file = True
                    break
                result.append(int(number))

            result.sort(reverse=False)
            filename = f'part-{num}'
            LOGGER.info(f"Save to {filename} with size: {len(result)} numbers")
            with open(path.join(tmp_dir, filename), 'w') as out_f:
                out_f.writelines(map(lambda v: f"{str(v)}\n", result))


def merge(tmp_dir, output_dir, filename):
    """
    Merge several ordered files into single one.
    Args:
        tmp_dir: Required. Directory with the small ordered files.
        output_dir: Required. Directory for storing result single file.
        filename: Required. Origin file name.

    """
    providers = []

    for path_to_part in glob.iglob(f"{tmp_dir}/part-*"):
        fd = open(path_to_part, 'r')
        provider = DataProvider(fd, int(fd.readline()))
        providers.append(provider)

    output_file = path.join(output_dir, f'sorted-{filename}')
    buffer = []
    with open(output_file, 'w') as out_f:
        count = 0
        while providers:
            min_idx: Union[int, None] = None
            for idx, provider in enumerate(providers):
                if not min_idx or providers[min_idx].cur_value > provider.cur_value:
                    min_idx = idx

            count += 1
            if count % BATCH_SIZE_FOR_FLUSH == 0:
                LOGGER.info(f"Output file size: {round(os.stat(output_file).st_size / 1024 / 1024, 2)} Mb ")

            prev_value = None

            while prev_value is None or prev_value == providers[min_idx].cur_value:
                buffer.append(f"{str(providers[min_idx].cur_value)}\n")
                if len(buffer) > BATCH_SIZE_FOR_FLUSH:
                    out_f.writelines(buffer)
                    buffer = []
                prev_value, providers[min_idx].cur_value = providers[min_idx].cur_value, int(
                    providers[min_idx].fd.readline())

            if not providers[min_idx].cur_value:
                LOGGER.info(f"Close provider with ID: {min_idx}")
                providers[min_idx].fd.close()
                del providers[min_idx]

        if len(buffer):
            out_f.writelines(buffer)
