from collections.abc import Iterable
from datetime import datetime

from src.spi_command import Command


class Trace(list):
    def __init__(self, start_time : float) -> None:
        super().__init__()
        # float, int -> epoch time, convert to datetime string
        if isinstance(start_time, (float, int)):
            self.time = self._convert_epoch_to_datetimestr(start_time)
        # str -> datetime string, validate format, raise exception if it does not match
        elif isinstance(start_time, str):
            self.time = self._validate_datetimestr_format(start_time, "%Y-%m-%dT%H_%M_%SS%f")


    def _validate_datetimestr_format(self, datetime_string : str, format_string : str) -> str:
        try:
            datetime.strptime(datetime_string, format_string)
            return datetime_string
        except ValueError as e:
            raise ValueError(f"{datetime_string} does not match with format: {format_string}") from e
    
    def _convert_epoch_to_datetimestr(self, epoch_time : float) -> str:
        datetime_object = datetime.fromtimestamp(epoch_time)
        milliseconds = datetime_object.microsecond // 1000
        return datetime_object.strftime("%Y-%m-%dT%H_%M_%SS") + f"{milliseconds:03d}"
        
    def __setitem__(self, index : int, spicommand : Command) -> None:
        super().__setitem__(index, self._validate_type(spicommand, Command))

    def insert(self, index : int, spicommand : Command) -> None:
        super().insert(index, self._validate_type(spicommand, Command))

    def append(self, spicommand : Command) -> None:
        super().append(self._validate_type(spicommand, Command))

    def extend(self, other: Iterable) -> None:
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(self._validate_type(spicommand, Command) for spicommand in other)

    def _validate_type(self, value : any, datatype : any):
        if isinstance(value, datatype):
            return value
        raise TypeError(f"{datatype} expected, got {type(value)}")
