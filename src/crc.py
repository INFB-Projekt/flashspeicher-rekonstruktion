from loguru import logger
import sys


class CRC:
    def __init__(self, log=None):
        if log is None:
            logger.remove()  # All configured handlers are removed
            logger.add(sys.stderr, format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
                                          "<cyan>{function}</cyan>:<cyan>{line}</cyan>: <level>{message}</level>",
                       level="ERROR")

    @staticmethod
    def reflect_byte(byte):
        return int('{:08b}'.format(byte)[::-1], 2)

    @staticmethod
    def calc_crc8(hex_string, poly=0x07, init=0x00, ref_in=False, ref_out=False, xor_out=0x00):
        data = bytes.fromhex(hex_string)
        crc = init

        for byte in data:
            if ref_in:
                byte = CRC.reflect_byte(byte)

            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFF

        if ref_out:
            crc = CRC.reflect_byte(crc)

        return f"0x{crc ^ xor_out:02X}"

    @staticmethod
    def calc_crc16(hex_string, poly=0x8005, init=0x0000, ref_in=True, ref_out=True, xor_out=0x0000):
        def reflect_byte(byte):
            return int('{:08b}'.format(byte)[::-1], 2)

        data = bytes.fromhex(hex_string)
        crc = init

        for byte in data:
            if ref_in:
                byte = reflect_byte(byte)

            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFFFF

        if ref_out:
            crc = reflect_byte(crc >> 8) | (reflect_byte(crc & 0xFF) << 8)

        return f"0x{crc ^ xor_out:04X}"

    @staticmethod
    def calc(data):
        if data.startswith("0x"):
            data = data[2:]
        if len(data) > 100:
            return CRC.calc_crc16(data)
        return CRC.calc_crc8(data)

    @staticmethod
    def is_valid(data: str, crc: str):
        logger.debug(crc)
        crc = (crc if crc.startswith("0x") else "0x" + crc).lower()
        logger.debug(f"trying to validate crc of {data}")
        logger.debug(f"crc should be {crc}")
        calculated_crc = CRC.calc(data).lower()
        logger.debug(f"calculated crc: {calculated_crc}")

        return crc == calculated_crc
