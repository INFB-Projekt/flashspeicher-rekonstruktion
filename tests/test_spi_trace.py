import pytest

import sys
sys.path.append('./src/')

from spi_trace import Trace
from spi_command import Command, Instruction, Payload


def test_correct_init_trace():
    trace = Trace(1234567890)
    assert isinstance(trace, Trace)


def test_incorrect_init_trace():
    with pytest.raises(TypeError):
        Trace()

    with pytest.raises(ValueError):
        # init trace with false format
        Trace("2023-06-19T16:52:37s12345")


def get_correct_command_instance() -> Command:
    instruction = Instruction(hex(0x58), hex(0xc0ffee), hex(0x92))
    payload = [Payload(hex(0x1234567890), hex(0xad))]
    return Command(relative_time=0.001, instruction=instruction, payload=payload)


def get_correct_trace_instance() -> Trace:
    return Trace(1234567890)

def get_filled_trace() -> Trace:
    trace = get_correct_trace_instance()

    for i in range(10):
        trace.append(get_correct_command_instance())

    return trace

def test_append_spi_command():
    command = get_correct_command_instance()
    trace = get_correct_trace_instance()

    trace.append(command)

    assert len(trace) == 1
    assert trace[0] == command


def test_append_false_type():
    any = object
    trace = get_correct_trace_instance()

    with pytest.raises(TypeError):
        trace.append(any)

def test_insert_spi_command():
    command = get_correct_command_instance()
    filledTrace = get_filled_trace()

    filledTrace.insert(5, command)

    assert filledTrace[5] == command
    assert filledTrace[4] != command


def test_insert_false_type():
    any = object
    trace = get_filled_trace()

    with pytest.raises(TypeError):
        trace.insert(5, any)


def test_extend_spi_commands():
    first_trace = get_filled_trace()
    second_trace = get_filled_trace()

    len_first_trace = len(first_trace)

    first_trace.extend(second_trace)

    assert first_trace[len_first_trace] == second_trace[0]
    assert first_trace[-1:] == second_trace[-1:]


def test_extend_false_type():
    first_trace = get_filled_trace()
    any_list = [object, int, str, 123, "abc"]

    with pytest.raises(TypeError):
        first_trace.extend(any_list)


def test_extend_list_of_commands():
    command_list = []
    for i in range(10):
        command_list.append(get_correct_command_instance())

    trace = get_correct_trace_instance()

    trace.extend(command_list)

    assert len(trace) == 10

