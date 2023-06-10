import pytest
from src.reconstruction_dummy import *
from src import reconstruction_dummy
import filecmp
import shutil



@pytest.mark.parametrize("input_value, expected_result", [
    (1684412522000, "1684412521519.csv"),
    (1684180607000, pytest.raises(Exception)),
    (1684412557500, "1684412557428.csv")
])

def test_find_csv_file(input_value, expected_result):
    csv__working_dummy_list = ["1684180607266.csv", "1684412450615.csv", "1684412490294.csv", "1684412497437.csv", "1684412505107.csv",
                      "1684412521519.csv", "1684412535134.csv", "1684412541025.csv", "1684412549983.csv", "1684412554197.csv", "1684412557428.csv"]
    reconstruction_dummy.reconstruction_timestamp = input_value

    if(input_value == 1684180607000):
        with pytest.raises(Exception):
            find_csv_file(csv__working_dummy_list)
    else:
        result = find_csv_file(csv__working_dummy_list)

        assert result == expected_result


@pytest.mark.parametrize("input_value, expected_result", [
    (1684412541000, pytest.raises(Exception)),
    (1684412541045, 19),
    (1684412551025, 100)
])

def test_find_target_row(input_value, expected_result):
    reconstruction_dummy.reconstruction_timestamp = input_value
    target_csv = "./tests/resources/1684412541025.csv"
    if(input_value == 1684412541000):
        with pytest.raises(Exception):
            find_target_row("1684412541025.csv", target_csv)
    else:
        result = find_target_row("1684412541025.csv", target_csv)

        assert result == expected_result



def test_reconstruction():
    
    csv = "./tests/resources/test_trace.csv"
    result = "./tests/resources/result_image.img"
    copyImg = "./tests/resources/copyImg.img"

    shutil.copy("./tests/resources/orgImg.img", copyImg)

    reconstruction_dummy.image_path = copyImg

    reconstruction(-1, csv)

    assert filecmp.cmp(copyImg, result)

    os.remove(copyImg)











