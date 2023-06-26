import pytest
from src.dump_converter import *


# test single- and multi-block writes separately to better see where the error would be
# the bin to hex converter is implicitly also tested through this.
# It will only yield the correct amount of writes if the bin to hex is (somewhat) correct
path_to_dumps = "/resources/hex/"  # change this to "resources/bin" to also implicitly test the bin to hex converter

bin_fname_to_amount_multi_block_writes = {  # amount of writes found by manually analyzing of the .sal trace
    "2023-06-19T16-53-09s180550.csv": 1,
    "2023-06-19T16-53-20s861052.csv": 2,
    "2023-06-19T16-53-30s004624.csv": 2,
    "2023-06-19T16-54-09s942272.csv": 1,
}

bin_fname_to_amount_single_block_writes = {  # amount of writes found by manually analyzing of the .sal trace
    "2023-06-19T16-52-37s927030.csv": 4,
    "2023-06-19T16-52-51s561826.csv": 4,
    "2023-06-19T16-52-58s817711.csv": 4,
    "2023-06-19T16-53-09s180550.csv": 6,  # 6 without multi-block write
    "2023-06-19T16-53-20s861052.csv": 4,  # 4 without multi
    "2023-06-19T16-53-30s004624.csv": 5,  # 5 without multi
    "2023-06-19T16-53-51s010233.csv": 8,
    "2023-06-19T16-54-09s942272.csv": 7,  # 7 without multi
}


def test_extract_writes_single_only():
    for fname, amount_writes in bin_fname_to_amount_single_block_writes.items():
        print("testing", fname)
        d = Dump(path_to_dumps + fname, is_hex=True)  # set is_hex=False to implicitly test the bin to hex converter
        # d.export("resources/hex/" + fname)
        trace = d.extract_writes(single_only=True)
        assert amount_writes == len(trace)
        print("pass", fname)


def test_extract_writes_multi_only():
    for fname, amount_writes in bin_fname_to_amount_multi_block_writes.items():
        print("testing", fname)
        d = Dump(path_to_dumps + fname, is_hex=True)  # set is_hex=False to implicitly test the bin to hex converter
        # d.export("resources/hex/" + fname)
        trace = d.extract_writes(multi_only=True)
        assert amount_writes == len(trace)
        print("pass", fname)
