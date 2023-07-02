import sys
import pandas as pd
from time import time
from loguru import logger

from utils import two_digit_hex_str, concat_df_key_to_hex, get_timestamp_from_path
from crc import CRC
from spi_command import Instruction, Command, Payload
from spi_trace import Trace


class Dump:  # creating a Dump instance from binary may take a while for converting it to hex
    def __init__(self, path: str, level="INFO", is_hex=False):
        logger.remove()  # All configured handlers are removed
        logger.add(sys.stderr, format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
                              "<cyan>{function}</cyan>:<cyan>{line}</cyan>: <level>{message}</level>", level=level)

        self.payload_len = 512

        logger.info("reading csv")
        if is_hex:
            self.hex = pd.read_csv(path)
        else:
            self.binary = pd.read_csv(path)
            logger.info("converting to hex, this may take a while")
            self.hex = self._to_hex()
        
        try:
            self.trace = Trace(get_timestamp_from_path(path))
        except ValueError as e:
            # ValueError-Exception contains given datetime string and expected datetime format 
            logger.debug(str(e))
            logger.info("set the time of the trace to the current time")
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

    def get_start_token_loc(self, index: int, start_token: str = "0xfe") -> int:
        max_index = index + 128  # randomly assume that there is a max of 128 bytes of noise before start token is sent
        start_token_loc = 0
        for i in range(index, max_index):
            try:
                current_mosi = self.hex.loc[i]["MOSI"]
            except (ValueError, KeyError):
                break  # we exceeded the end of the dataframe
            if current_mosi == start_token:
                start_token_loc = i
                break
        return start_token_loc

    def add_write(self, index, payloads, multi=False):
        time = self.hex.loc[index]["time"]
        opcode = self.hex.loc[index]["MOSI"]
        params = concat_df_key_to_hex(self.hex.loc[index + 1:index + 4], "MOSI")
        if multi:
            logger.success(
                f"multi-block write at time {time} with {len(payloads)} payloads seems valid, adding to trace")
        else:
            logger.success(f"single-block write at {time} seems valid, adding to trace")
        instruction = Instruction(opcode, params,
                                  CRC.calc(opcode[2:] + params[2:]))  # TODO: use actual crc here, once crc function works
        command = Command(time, instruction, payloads)
        self.trace.append(command)

    def handle_multi_block_write(self, index, row):
        payloads = []
        start_token_loc = self.get_start_token_loc(index, "0xfc")
        while start_token_loc > 0:
            payload = concat_df_key_to_hex(self.hex.loc[start_token_loc + 1:start_token_loc + self.payload_len], "MOSI")
            try:
                crc_start = start_token_loc + self.payload_len + 1
                crc = concat_df_key_to_hex(self.hex.loc[crc_start:crc_start + 1], "MOSI")
            except KeyError:
                logger.debug("Exceeded dataframe length when trying to get CRC")
                return
            has_valid_crc = CRC.is_valid(payload, crc)
            has_valid_crc = True  # TODO: delete this override once CRC.calc() works correctly
            if has_valid_crc:
                payloads.append(Payload(payload, CRC.calc(payload)))
            start_token_loc = self.get_start_token_loc(start_token_loc + self.payload_len + 2, "0xfc")  # 2 byte crc
        if len(payloads) < 1:
            logger.debug(f"not a single valid payload for proposed multi block write at {row['time']}")
            return
        self.add_write(index, payloads, multi=True)

    def handle_single_block_write(self, index, row):
        start_token_loc = self.get_start_token_loc(index, "0xfe")
        if start_token_loc <= 0:
            logger.debug(f"no start token found for potential write at relative time: {row['time']}, skipping")
            return  # no start token found within 128 bytes --> continue with next potential write

        payload_len = 512
        payload = concat_df_key_to_hex(self.hex.loc[start_token_loc + 1:start_token_loc + payload_len], "MOSI")
        try:
            crc_start = start_token_loc + payload_len + 1
            crc = concat_df_key_to_hex(self.hex.loc[crc_start:crc_start + 1], "MOSI")
        except KeyError:
            logger.debug("Exceeded dataframe length when trying to get CRC")
            return
        has_valid_crc = CRC.is_valid(payload, crc)
        has_valid_crc = True  # TODO: delete this override once CRC.calc() works correctly
        if has_valid_crc:
            self.add_write(index, [Payload(payload, CRC.calc(payload))], multi=False)
        else:
            logger.debug(f"invalid crc for potential write at relative time: {row['time']}, skipping")

    def extract_writes(self, single_only=False, multi_only=False) -> Trace:
        logger.info("extracting writes")
        potential_writes = self.hex[self.hex["MOSI"].isin(["0x58", "0x59"])]
        logger.info(f"found {len(potential_writes)} potential writes")
        logger.info("checking potential writes for validity")

        for index, row in potential_writes.iterrows():
            logger.debug(f"----analyzing potential write at {row['time']}----")
            if row["MOSI"] == "0x58" and not multi_only:
                self.handle_single_block_write(index, row)
            elif row["MOSI"] == "0x59" and not single_only:
                self.handle_multi_block_write(index, row)

        logger.success(f"found {len(self.trace)} valid writes")
        return self.trace

    def export(self, path: str):
        self.hex.to_csv(path)
        logger.info(f"exported hex dump to {path}")
