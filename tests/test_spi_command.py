import pytest
from src.spi_command import Command, Instruction, Payload
from src.crc import CRC

# help functions
def get_correct_command_instance(rel_time: float) -> Command:
    instruction = Instruction(hex(0x58), hex(0xc0ffee), hex(0x92))
    payload = [Payload(hex(0x1234567890), hex(0xad))]
    return Command(relative_time=rel_time, instruction=instruction, payload=payload)

def calculate_correct_crc(hexstring : str) -> str:
    return "0x" + CRC.calc(hexstring).lower()


def test_instruction_correct_init():
    opcode = hex(0x58)
    parameter = hex(0xc0ffee)
    hexstring_for_crc = opcode + parameter.replace("0x", "")
    crc = calculate_correct_crc(hexstring_for_crc)
    instruction = Instruction(opcode, parameter, crc)

    assert isinstance(instruction, Instruction)

def test_instruction_incorrect_init():
    with pytest.raises(Exception):
        Instruction(hex(0x58), hex(0xc0ffee), hex(0x00))


def test_payload_correct_init():
    data = hex(0x1234567890)
    crc = CRC.calc(data)

    payload = Payload(data, crc)

    assert isinstance(payload, Payload)


def test_payload_incorrect_init():
    data = hex(0x1234567890)

    with pytest.raises(Exception):
        payload = Payload(data, hex(0x00))


def test_command_init_single_payload():
    opcode = hex(0x58)
    parameter = hex(0xc0ffee)
    hexstring_for_crc = opcode + parameter.replace("0x", "")
    crc = calculate_correct_crc(hexstring_for_crc)
    correct_instruction = Instruction(opcode, parameter, crc)

    data = hex(0x1234567890)
    crc = CRC.calc(data)

    correct_payload = Payload(data, crc)

    relative_time = 0.1

    command = Command(relative_time=relative_time, 
                      instruction=correct_instruction, 
                      payload=[correct_payload])
    
    assert isinstance(command, Command)


def test_command_init_multi_payload():
    opcode = hex(0x58)
    parameter = hex(0xc0ffee)
    hexstring_for_crc = opcode + parameter.replace("0x", "")
    crc = calculate_correct_crc(hexstring_for_crc)
    correct_instruction = Instruction(opcode, parameter, crc)

    payload_list = []
    for i in range(5):
        data = hex(0x1234567890)
        crc = CRC.calc(data)

        payload_list.append(Payload(data, crc))

    relative_time = 0.1

    command = Command(relative_time=relative_time, 
                      instruction=correct_instruction, 
                      payload=payload_list)
    
    assert isinstance(command, Command)
