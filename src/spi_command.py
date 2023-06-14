from crc import CRC


class Instruction:
    def __init__(self, opcode : hex, parameter : hex, crc : hex) -> None:
        self._check_crc(opcode, parameter, crc) 
        self.opcode = opcode
        self.parameter = parameter

    def _check_crc(self, opcode : hex, parameter : hex, crc : hex) -> None:
        concatenate_hex = self._concatenate_hex(opcode, parameter)
        
        if not CRC.is_valid(concatenate_hex, crc):
            raise Exception (
                "CRC is not valid"
            )
 
    def _concatenate_hex(self, first_hex : hex, second_hex : hex) -> hex:
        return first_hex[2:] + second_hex[2:]
    

class Payload:
    def __init__(self, data : hex, crc : hex) -> None:
        self._check_crc(data, crc)
        self.data = data

    def _check_crc(self, data : hex, crc : hex) -> None:
        if not CRC.is_valid(data, crc):
            raise Exception (
                "CRC is not valid"
            )


class Command:
    def __init__(self, relative_time : float, instruction : Instruction, payload : list[Payload]) -> None:
        self.relative_time = relative_time
        self.instruction = instruction
        self.payload = self._concatenate_payload(payload)

    def _concatenate_payload(self, payload : list[Payload]) -> hex:
        concatenate_payload = "0x"
        for p in payload:
            concatenate_payload += p.data.replace("0x", "")
        
        return concatenate_payload

    def __str__(self) -> str:
        header = "time\topcode\tparameter\tpayload\n"     
        body = f"{self.relative_time}\t{self.instruction.opcode}\t{self.instruction.parameter}\t{self.payload[:5] + self.payload[-5:]}\n"
        return header + body

        



