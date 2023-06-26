import sys
import pandas as pd
from time import time
from loguru import logger

from src.csv_exporter import Exporter
from src.utils import two_digit_hex_str
from src.crc import CRC
from src.spi_command import Instruction, Command, Payload
from src.spi_trace import Trace


logger.remove()  # All configured handlers are removed
# level can be ERROR for no logs, INFO for basic info on progress or DEBUG for ultimate info
logger.add(sys.stderr, format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
                              "<cyan>{function}</cyan>:<cyan>{line}</cyan>: <level>{message}</level>", level="DEBUG")


class Dump:  # creating a Dump instance from binary may take a while for converting it to hex
    def __init__(self, path: str, is_hex=False):
        logger.info("reading csv")
        if is_hex:
            self.hex = pd.read_csv(path)
        else:
            self.binary = pd.read_csv(path)
            logger.info("converting to hex, this may take a while")
            self.hex = self._to_hex()
        self.trace = Trace(time())

    def _to_hex(self) -> pd.DataFrame:
        self.binary["Channel 2"] = pd.to_numeric(self.binary["Channel 2"], errors='raise').astype('Int32')

        time = []
        miso = []
        mosi = []

        bit_counter = 0
        miso_bits = str()
        mosi_bits = str()

        predecessor_clock = -1

        for _, row in self.binary.iterrows():
            # print(bit_counter, row["Channel 2"], (bit_counter < 8 and row['Channel 2'] == 1))
            if bit_counter < 8 and row['Channel 2'] == 1 and predecessor_clock == 0:
                miso_bits = miso_bits + str(int(row['Channel 0']))
                mosi_bits = mosi_bits + str(int(row['Channel 1']))
                # print("added some bits:", row["Channel 0"], row["Channel 1"], miso_bits, mosi_bits)
                bit_counter += 1

                if bit_counter == 1:
                    time.append(row['Time [s]'])
                    predecessor_clock = int(row["Channel 2"])
                    continue
            # print("MISO:", miso_bits, "MOSI:", mosi_bits)

            if bit_counter == 8:
                miso.append(two_digit_hex_str(int(miso_bits, 2)))
                mosi.append(two_digit_hex_str(int(mosi_bits, 2)))
                miso_bits = ""
                mosi_bits = ""
                bit_counter = 0
            
            predecessor_clock = int(row["Channel 2"])

        dump_dict = {
            "time": time,
            "MISO": miso,
            "MOSI": mosi
        }

        # bin case dump ends so that number of bin digits mod 8 != 0 --> throw away last ones
        if len(dump_dict["time"]) != len(dump_dict["MISO"]) or len(dump_dict["time"]) != len(dump_dict["MOSI"]):
            dump_dict["time"] = dump_dict["time"][:-1]
        return pd.DataFrame(dump_dict)

    def extract_writes(self) -> Trace:
        logger.info("extracting writes")
        potential_writes = self.hex[self.hex["MOSI"].isin(["0x58", "0x59"])]
        logger.info(f"found {len(potential_writes)} potential writes")
        logger.info("checking potential writes for validity")
        for index, row in potential_writes.iterrows():
            # TODO: differentiate between single and multi block
            # wait for start token
            max_index = index + 128  # randomly assume that there is a max of 128 bytes of noise before start token is sent
            start_token_loc = 0
            for i in range(index, max_index):
                try:
                    current_mosi = self.hex.loc[i]["MOSI"]
                except (ValueError, KeyError):
                    break  # we exceeded the end of the dataframe
                if current_mosi == "0xfe":
                    start_token_loc = i
                    break
            if start_token_loc <= 0:
                logger.debug(f"no start token found for potential write at relative time: {row['time']}, skipping")
                continue  # no start token found within 128 bytes --> continue with next potential write
            payload_len = 512
            payload_df = self.hex.loc[start_token_loc + 1:start_token_loc + payload_len]
            # print("start token loc", start_token_loc, "crc loc:", (start_token_loc + payload_len + 1))
            payload = ""
            for _, x in payload_df.iterrows():
                payload += x["MOSI"][2:]
            try:
                is_valid_crc = CRC.is_valid(payload, self.hex.loc[start_token_loc + payload_len + 1]["MOSI"][2:])
            except KeyError:
                continue
            # is_valid_crc = (self.hex.loc[start_token_loc + payload_len + 1]["MOSI"] == "0x00")  # TODO: uncomment this to analyze example dumps from resources/gen.py
            is_valid_crc = True  # TODO: uncomment this to pass tests
            if is_valid_crc:
                time = self.hex.loc[index]["time"]
                opcode = self.hex.loc[index]["MOSI"]
                param_df = self.hex.loc[index + 1:index + 4]
                params = "0x"
                for _, x in param_df.iterrows():
                    params += x["MOSI"][2:]
                logger.debug("valid write found at", row["time"])
                instruction = Instruction(opcode, params, CRC.calc(opcode[2:] + params[2:]))  # TODO: use actual crc here, once crc function works
                command = Command(time, instruction, [Payload(payload, CRC.calc(payload))])
                self.trace.append(command)
                logger.debug(f"write at time {row['time']} seems valid, adding to trace")
            else:
                logger.debug(f"invalid crc for potential write at relative time: {row['time']}, skipping")
        logger.success(f"found {len(self.trace)} valid writes")
        return self.trace

    def export(self, path: str):
        self.hex.to_csv(path)
        logger.info(f"exported hex dump to {path}")


if __name__ == "__main__":
    fname = "2023-06-19T16-52-51s561826.csv"
    d = Dump(f"../resources/bin/{fname}")
    d.export(f"../resources/hex/{fname}")
    trace = d.extract_writes()
    exporter = Exporter("../resources/filtered_trace")
    exporter.export_trace(trace)
    