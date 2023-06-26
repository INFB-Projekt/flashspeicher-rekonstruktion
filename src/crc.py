import sys
import crcmod
from loguru import logger


class CRC:
    def __init__(self, log=None):
        if log is None:
            logger.remove()  # All configured handlers are removed
            logger.add(sys.stderr, format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
                                          "<cyan>{function}</cyan>:<cyan>{line}</cyan>: <level>{message}</level>",
                       level="ERROR")

    @staticmethod
    def calc(data: str) -> str:
        if data.startswith("0x"):
            data = data.replace("0x", "")
        crc_func = crcmod.predefined.mkPredefinedCrcFun('crc-8')
        message = bytearray.fromhex(data)
        # calc crc using crc8 algo
        crc = crc_func(message)
        # print(crc)
        crc_hex = hex(crc)[2:].zfill(2)
        # print("crc:", crc_hex)
        return crc_hex.upper()

    @staticmethod
    def calc2(data: str):
        # The polynomial used for SPI CRC is x^15 + x^14 + x^13 + x^12 + x^11 + x^10 + x^9 + x^8 + x^7 + x^6 + x^5 + x^4 + x^3 + x^2 + x^1 + x^0.
        polynomial = 16

        # Initial CRC value is zero.
        init_crc = 0x0000

        # Create a CRC function using the polynomial and initial value.
        crc_func = crcmod.mkCrcFun(polynomial, initCrc=init_crc, rev=True)

        return crc_func(data)

    @staticmethod
    def calc3(data):
        crc8 = crcmod.Crc(0x12F, initCrc=0)  # 0x12F = 100101111 = x^8 + x^5 + x^3 + x^2 + x + 1
        crc8.update('123456789')
        print(hex(crc8.crcValue))

    @staticmethod
    def preprocess_data(data):
        i = 0
        output = []
        while i < len(data) - 2:
            output.append(int(data[i:i+2], 16))
            i+= 2
        print(output)
        return output

    @staticmethod
    def calc4(data):
        data = CRC.preprocess_data(data)
        crc = 0x00
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x07
                else:
                    crc = crc << 1
        print(crc)
        return crc

    @staticmethod
    def is_valid(data: str, crc: str) -> bool:
        logger.debug(f"trying to validate crc of {data}")
        logger.debug(f"crc should be {crc}")
        data = data.replace("0x", "")
        crc = crc.replace("0x", "").lower()
        calculated_crc = CRC.calc(data).lower()
        logger.debug(f"calculated crc: {calculated_crc}")
        return crc == calculated_crc


if __name__ == "__main__":
    CRC.calc("2e202020202020202020201000009d8ecc56cc5600009d8ecc568f00000000002e2e2020202020202020201000009d8ecc56cc5600009d8ecc56000000000000e56500780061006d0070000f005a6c0065002e0074007800740000000000ffffe558414d504c45205458542000009d8ecc56cc5600009d8ecc56000000000000e5780074000000ffffffff0f00c8ffffffffffffffffffffffff0000ffffffffe5720065006e0061006d000f00c865006400460069006c00650000002e007400e5454e414d457e31545854200000938ecc56cc560000938ecc568e000a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
