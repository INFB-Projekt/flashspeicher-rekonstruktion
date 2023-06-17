from src.spi_trace import Trace
from src.spi_command import Command
import csv
from os import path, makedirs

class Exporter():

    def __init__(self, destination_path : str) -> None:
        self._destination_path = self._validate_path(destination_path)
        
        
    def export_trace(self, trace : Trace) -> None:
        output_file = path.join(self._destination_path, f"{trace.time}.csv")
        self._create_directories()
        
        with open(output_file, "w", newline='') as f:
            writer = csv.writer(f, delimiter=';')

            # header
            writer.writerow(["time", "opcode", "param", "payload"])

            # body
            for command in trace:
                writer.writerow(self._get_elements_as_list(command))


    def set_destination_path(self, path : str) -> None:
        self._destination_path = self._validate_path(path)



    def _validate_path(self, path_to_validate : str) -> str:
        if not '.' in path.basename(path_to_validate):
            return path_to_validate
        raise NotADirectoryError(
            f"{path_to_validate} need to be a path to a directory"
        )

    def _create_directories(self):
        if not path.exists(self._destination_path):
            makedirs(self._destination_path)


    def _get_elements_as_list(self, command : Command) -> list[str]:
        relative_time = str(command.relative_time)
        opcode = str(command.instruction.opcode)
        parameter = str(command.instruction.parameter)
        payload = str(command.payload)

        return [relative_time, opcode, parameter, payload]    
    
