import os
import shutil
import pytest
from src.spi_trace import Trace
from src.csv_exporter import Exporter
from src.spi_command import Command, Instruction, Payload


# Help Functions
def get_filled_trace(timestamp: int, size: int = 10) -> Trace:
    trace = Trace(timestamp)

    for i in range(size):
        command = get_correct_command_instance(rel_time=i)
        trace.append(command)

    return trace

def get_correct_command_instance(rel_time: float) -> Command:
    instruction = Instruction(hex(0x58), hex(0xc0ffee), hex(0x92))
    payload = [Payload(hex(0x1234567890), hex(0xad))]
    return Command(relative_time=rel_time, instruction=instruction, payload=payload)

def clean_up_old_test_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)

def get_output_dir_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dir_name = "output_exporter"

    return os.path.join(current_dir, dir_name)


# Test Class
class TestCsvExporter:
    def test_export_trace(self):
        test_dir_path = get_output_dir_path()

        clean_up_old_test_dir(test_dir_path)

        timestamp = 123456789
        trace = get_filled_trace(timestamp, 20)

        exporter = Exporter(test_dir_path)

        exporter.export_trace(trace)

        assert os.path.exists(test_dir_path)
        file_path = os.path.join(test_dir_path, f"{timestamp}.csv")
        assert os.path.exists(file_path)

        clean_up_old_test_dir(test_dir_path)

    def test_csv_data(self):
        test_dir_path = get_output_dir_path()

        clean_up_old_test_dir(test_dir_path)

        timestamp = 123
        trace = Trace(timestamp)
        command = get_correct_command_instance(rel_time=0)
        trace.append(command)

        exporter = Exporter(test_dir_path)
        exporter.export_trace(trace)

        file_path = os.path.join(test_dir_path, f"{timestamp}.csv")

        with open(file_path, "r") as f:
            lines = f.readlines()

            header = lines[0].replace("\n", "")
            body = lines[1].replace("\n", "")

        correct_header = ["time", "opcode", "param", "payload"]
        correct_body = [str(command.relative_time),
                        str(command.instruction.opcode),
                        str(command.instruction.parameter),
                        str(command.payload)]

        header = header.split(";")
        body = body.split(";")

        assert correct_header == header, f"CSV-Header does not match the standard: {str(correct_header)}"
        assert correct_body == body, f"CSV-Body does not match the standard: {str(correct_body)}"

        clean_up_old_test_dir(test_dir_path)