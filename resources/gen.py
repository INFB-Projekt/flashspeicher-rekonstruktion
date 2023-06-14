from random import randint
import csv


class command_package:
    command_byte: str
    addr_1: str
    addr_2: str
    addr_3: str
    addr_4: str
    crc: str


class data_package:
    start_token = "0xfe"
    data = []
    crc: str


def generate():
    csv_file = open('in/spi_trace.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Time [s]", "Channel 0", "Channel 1", "Channel 2"])  # Channel 0 = MISO, Channl 1 = MOSI

    for i in range(5):
        cp = command_package()
        dp = data_package()

        cp.command_byte = hex(88)
        cp.addr_1 = hex(randint(0, 255))
        cp.addr_2 = hex(randint(0, 255))
        cp.addr_3 = hex(randint(0, 255))
        cp.addr_4 = hex(randint(0, 255))
        cp.crc = "0x00"

        for i in range(512):
            dp.data.append(hex(randint(0, 255)))
        dp.crc = "0x00"

        write_csv(cp, dp, csv_writer)
    csv_file.close()


def write_csv(cp: command_package, dp: data_package, csv_writer):
    for i in range(randint(0, 2)):
        write_bits("0xff", "0xff", csv_writer)

    write_bits("0xff", cp.command_byte, csv_writer)
    write_bits("0xff", cp.addr_1, csv_writer)
    write_bits("0xff", cp.addr_2, csv_writer)
    write_bits("0xff", cp.addr_3, csv_writer)
    write_bits("0xff", cp.addr_4, csv_writer)
    write_bits("0xff", cp.crc, csv_writer)

    for i in range(randint(0, 2)):  # random noise until data transfer starts
        write_bits("0xff", "0xff", csv_writer)

    write_bits("0x00", "0xff", csv_writer)  # what does this do?

    for i in range(randint(0, 2)):  # random noise until data transfer starts??
        write_bits("0xff", "0xff", csv_writer)

    write_bits("0xff", dp.start_token, csv_writer)  # send start token. is this correct? Does the start token come through MOSI?

    for i in range(512):  # send 512 bytes of data
        write_bits("0xff", dp.data[i], csv_writer)

    write_bits("0xff", dp.crc, csv_writer)  # send crc

    for i in range(randint(0, 2)):  # random noise
        write_bits("0xff", "0xff", csv_writer)

    write_bits("0x40", "0xff", csv_writer)  # set idle state?? is this according to the protocol? Isn't idle stat only set once in the beginning?

    for i in range(randint(0, 2)):  # random noise??
        write_bits("0xff", "0xff", csv_writer)


def write_bits(miso, mosi, csv_writer):
    miso_bits = bin(int(miso, 16))[2:].zfill(8)
    mosi_bits = bin(int(mosi, 16))[2:].zfill(8)
    rows = []
    for i in range(8):
        rows.append([0, miso_bits[i], mosi_bits[i], 1])
        rows.append([0, miso_bits[i], mosi_bits[i], 0])
    csv_writer.writerows(rows)


generate()
