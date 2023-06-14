import crcmod


class CRC:
    @staticmethod
    def calc(data: str) -> str:
        crc8_func = crcmod.predefined.mkPredefinedCrcFun('crc-8')
        message = bytearray.fromhex(data)
        # calc crc using crc8 algo
        crc = crc8_func(message)
        crc_hex = hex(crc)[2:].zfill(2)
        return crc_hex.upper()

    @staticmethod
    def is_valid(data: str, crc: str) -> bool:
        return crc.upper() == CRC.calc(data)
