import pytest

import os
import sys
sys.path.append('./src/')

from spi_trace import Trace
from csv_exporter import Exporter
from spi_command import Command, Instruction, Payload
from datetime import datetime


def get_formated_timestamp_string(epoch_time : float) -> str:
    datetime_object = datetime.fromtimestamp(epoch_time)
    milliseconds = datetime_object.microsecond // 1000
    return datetime_object.strftime("%Y-%m-%dT%H_%M_%SS") + f"{milliseconds:03d}"


# hardcoded variables for testing
timestamp = 1687262365.089078
format_timestamp = get_formated_timestamp_string(timestamp)


# Help Functions
def get_filled_trace(size: int = 10) -> Trace:
    trace = Trace(timestamp)

    for i in range(size):
        command = get_correct_command_instance(rel_time=i)
        trace.append(command)

    return trace

def get_correct_command_instance(rel_time: float) -> Command:
    instruction = Instruction(hex(0x58), hex(0xc0ffee), hex(0x92))
    payload = [Payload(hex(0x1234567890), hex(0xad))]
    return Command(relative_time=rel_time, instruction=instruction, payload=payload)

def remove_old_test_file() -> None:
    output_dir = get_output_dir_path()
    file_path = os.path.join(output_dir, f"{format_timestamp}.csv")
    if os.path.exists(file_path):
        os.remove(file_path)

def get_output_dir_path() -> str:
    return "./tests/resources"



# Test functions
def test_export_trace():
    output_dir = get_output_dir_path()

    remove_old_test_file()

    trace = get_filled_trace()

    exporter = Exporter(output_dir)

    exporter.export_trace(trace)

    file_path = f"{output_dir}/{format_timestamp}.csv"

    assert os.path.exists(file_path)


def test_csv_data():
    output_dir = get_output_dir_path()

    remove_old_test_file()

    trace = get_filled_trace()

    exporter = Exporter(output_dir)

    exporter.export_trace(trace)

    file_path = f"{output_dir}/{format_timestamp}.csv"

    with open(file_path, "r") as f:
        lines = f.readlines()

        header = lines[0].replace("\n", "")
        body = lines[1:]


    correct_header = ["time", "opcode", "param", "payload"]
    header = header.split(";")
    assert correct_header == header, f"CSV-Header does not match the standard: {str(correct_header)}"

    counter = 0
    for line in body:
        line = line.replace("\n", "")
        command = trace[counter]
        correct_body = [str(command.relative_time),
                        str(command.instruction.opcode),
                        str(command.instruction.parameter),
                        str(command.payload)]
        counter += 1 
        body_part = line.split(";")

        assert correct_body == body_part, f"CSV-Body does not match the standard: {str(correct_body)}"


def test_set_destination_path():
    output_path = get_output_dir_path()
    exporter = Exporter(output_path)

    wrong_destination = f"{output_path}/NotADirectory.txt"

    with pytest.raises(NotADirectoryError):
        exporter.set_destination_path(wrong_destination)

