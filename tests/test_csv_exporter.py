import os
import shutil
from src.spi_trace import Trace
from src.csv_exporter import Exporter
from src.spi_command import Command


class Test_Exporter:
    # Help Functions #
    # ----------------#

    def get_filled_trace(self, timestamp: int, size: int = 10) -> Trace:
        trace = Trace(timestamp)

        for i in range(size):
            command = Command(i, 0xc0ffee, 2**64 - 1)
            trace.append(command)

        return trace

    def clean_up_old_test_dir(self, path: str) -> None:
        if os.path.exists(path):
            shutil.rmtree(path)

    def get_output_dir_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        dir_name = "output_exporter"

        return os.path.join(current_dir, dir_name)

    # Test Functions #
    # ----------------#

    def test_export_trace(self):
        test_dir_path = self.get_output_dir_path()

        self.clean_up_old_test_dir(test_dir_path)

        timestamp = 123456789
        trace = self.get_filled_trace(timestamp, 20)

        exporter = Exporter(test_dir_path)

        exporter.export_trace(trace)

        assert os.path.exists(test_dir_path)
        file_path = os.path.join(test_dir_path, f"{timestamp}.csv")
        assert os.path.exists(file_path)

        self.clean_up_old_test_dir(test_dir_path)

    def test_csv_data(self):
        test_dir_path = self.get_output_dir_path()

        self.clean_up_old_test_dir(test_dir_path)

        timestamp = 123
        trace = Trace(timestamp)
        command = Command(0, 0xc0ffee, 2**64 - 1)
        trace.append(command)

        exporter = Exporter(test_dir_path)
        exporter.export_trace(trace)

        file_path = os.path.join(test_dir_path, f"{timestamp}.csv")

        with open(file_path, "r") as f:
            lines = f.readlines()

            header = lines[0].replace("\n", "")
            body = lines[1].replace("\n", "")

        correct_header = ["time", "opcode", "param", "payload"]
        correct_body = [str(command.relativ_time),
                        str(command.opcode),
                        str(command.parameter),
                        str(command.payload)]

        header = header.split(";")
        body = body.split(";")

        assert correct_header == header, f"CSV-Header erfüllt nicht den Standard: {str(correct_header)}"
        assert correct_body == body, f"CSV-Body erfüllt nicht den Standard: {str(correct_body)}"

        self.clean_up_old_test_dir(test_dir_path)
