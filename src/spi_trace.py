from collections.abc import Iterable
from src.spi_command import Command


class Trace(list):
    def __init__(self, start_time : int) -> None:
        super().__init__()
        self.time = self._validate_type(start_time, int)
        
    def __setitem__(self, index : int, spicommand : Command) -> None:
        super().__setitem__(index, self._validate_type(spicommand, Command))

    def insert(self, index : int, spicommand : Command) -> None:
        super().insert(index, self._validate_type(spicommand, Command))

    def append(self, spicommand : Command) -> None:
        super().append(self._validate_type(spicommand, Command))

    """
    Remove Extend Funktion, problematisch wegen dem Zeitstempel. Welchen Zeitstempel wollen wir nehmen?
    """ 
    def extend(self, other: Iterable) -> None:
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(self._validate_type(spicommand, Command) for spicommand in other)

    def _validate_type(self, value : any, datatype : any):
        if isinstance(value, datatype):
            return value
        raise TypeError(f"{datatype} expected, got {type(value)}")
