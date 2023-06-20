from src.spi_trace import Trace
from src.spi_command import Command
import csv
from os import path, makedirs
from datetime import datetime

class Exporter():

    def __init__(self, destination_path : str) -> None:
        self._destination_path = self._validate_path(destination_path)
        
        
    def export_trace(self, trace : Trace) -> None:
        datetime_timestamp = self._convert_epoch_to_datetimestr(trace.time)
        output_file = path.join(self._destination_path, f"{datetime_timestamp}.csv")
        self._create_missing_directories()
        
        with open(output_file, "w", newline='') as f:
            writer = csv.writer(f, delimiter=';')

            # header
            writer.writerow(["time", "opcode", "param", "payload"])

            # body
            for command in trace:
                writer.writerow(self._get_elements_as_list(command))


    def set_destination_path(self, path : str) -> None:
        self._destination_path = self._validate_path(path)

    def _convert_epoch_to_datetimestr(self, epoch_time : int) -> datetime:
        datetime_object = datetime.fromtimestamp(epoch_time)
        milliseconds = datetime_object.microsecond // 1000
        return datetime_object.strftime("%Y-%m-%dT%H_%M_%SS") + f"{milliseconds:03d}"

    def _validate_path(self, path_to_validate : str) -> str:
        if path.isdir(path_to_validate):
            return path_to_validate
        raise NotADirectoryError(
            f"{path_to_validate} need to be a path to a directory"
        )

    def _create_missing_directories(self):
        if not path.exists(self._destination_path):
            makedirs(self._destination_path)


    def _get_elements_as_list(self, command : Command) -> list[str]:
        relative_time = str(command.relative_time)
        opcode = str(command.instruction.opcode)
        parameter = str(command.instruction.parameter)
        payload = str(command.payload)

        return [relative_time, opcode, parameter, payload]    
    
