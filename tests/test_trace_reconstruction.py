import pytest
from src.trace_reconstruction import *
from src import trace_reconstruction
import filecmp
import shutil


@pytest.mark.parametrize("input_value, expected_result", [
    ("2023-05-18T14_22_02S000", "2023-05-18T14_22_01S000.csv"),
    ("2023-05-15T19_56_47S000", pytest.raises(Exception)),
    ("2023-05-18T19_56_47S000", "2023-05-18T14_22_37S000.csv")
])
def test_find_csv_file(input_value, expected_result):
    csv__working_dummy_list = ["2023-05-15T21_56_47S000.csv", "2023-05-18T14_20_50S000.csv", "2023-05-18T14_21_30S000.csv",
                               "2023-05-18T14_21_37S000.csv", "2023-05-18T14_21_45S000.csv",
                               "2023-05-18T14_22_01S000.csv", "2023-05-18T14_22_15S000.csv", "2023-05-18T14_22_21S000.csv",
                               "2023-05-18T14_22_29S000.csv", "2023-05-18T14_22_34S000.csv", "2023-05-18T14_22_37S000.csv"]
    trace_reconstruction.reconstruction_timestamp = datetime.datetime.strptime(input_value,
                                                                                        "%Y-%m-%dT%H_%M_%SS%f")

    if (input_value == "2023-05-15T19_56_47S000"):
        with pytest.raises(Exception):
            find_csv_file(csv__working_dummy_list)
    else:
        result = find_csv_file(csv__working_dummy_list)

        assert result == expected_result


@pytest.mark.parametrize("input_value, expected_result", [
    ("2023-05-18T13_22_21S025", pytest.raises(Exception)),
    ("2023-05-18T14_22_21S045", 19),
    ("2023-05-18T15_22_21S025", 100)
])
def test_find_target_row(input_value, expected_result):
    trace_reconstruction.reconstruction_timestamp = datetime.datetime.strptime(input_value,
                                                                                        "%Y-%m-%dT%H_%M_%SS%f")
    target_csv = "./tests/resources/2023-05-18T14_22_21S025.csv"
    if (input_value == "2023-05-18T13_22_21S025"):
        with pytest.raises(Exception):
            find_target_row("2023-05-18T14_22_21S025.csv", target_csv)
    else:
        result = find_target_row("2023-05-18T14_22_21S025.csv", target_csv)

        assert result == expected_result


def test_reconstruction():
    csv = "./tests/resources/test_trace.csv"
    result = "./tests/resources/result_image.img"
    copy_img = "./tests/resources/copyImg.img"

    shutil.copy("./tests/resources/orgImg.img", copy_img)

    trace_reconstruction.image_path = copy_img

    trace_reconstruction.reconstruction(-1, csv)

    assert filecmp.cmp(copy_img, result)

    os.remove(copy_img)
