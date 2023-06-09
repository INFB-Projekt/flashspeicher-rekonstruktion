import sys
import pytest
sys.path.append('./src/')

from dump_converter import *


# test single- and multi-block writes separately to better see where the error would be
# the bin to hex converter is implicitly also tested through this.
# It will only yield the correct amount of writes if the bin to hex is (somewhat) correct
path_to_dumps = "resources/hex/"  # change this to "resources/bin" to also implicitly test the bin to hex converter


@pytest.mark.parametrize("fname, amount_writes", [
    ("2023-06-19T16_52_37S927.csv", 4),
    ("2023-06-19T16_52_51S561.csv", 4),
    ("2023-06-19T16_52_58S817.csv", 4),
    ("2023-06-19T16_53_09S180.csv", 6),
    ("2023-06-19T16_53_20S861.csv", 4),
    ("2023-06-19T16_53_30S004.csv", 5),
    ("2023-06-19T16_53_51S010.csv", 8),
    ("2023-06-19T16_54_09S942.csv", 7),
])
def test_extract_writes_single_only(fname, amount_writes):
    print("testing", fname)
    d = Dump(path_to_dumps + fname, is_hex=True)  # set is_hex=False to implicitly test the bin to hex converter
    # d.export("resources/hex/" + fname)
    trace = d.extract_writes(single_only=True)
    assert amount_writes == len(trace)
    print("pass", fname)


@pytest.mark.parametrize("fname, amount_writes", [
    ("2023-06-19T16_53_09S180.csv", 1),
    ("2023-06-19T16_53_20S861.csv", 2),
    ("2023-06-19T16_53_30S004.csv", 2),
    ("2023-06-19T16_54_09S942.csv", 1),
])
def test_extract_writes_multi_only(fname, amount_writes):
    print("testing", fname)
    d = Dump(path_to_dumps + fname, is_hex=True)  # set is_hex=False to implicitly test the bin to hex converter
    trace = d.extract_writes(multi_only=True)
    assert amount_writes == len(trace)
    print("pass", fname)
