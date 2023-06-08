import pandas as pd
import crcmod
from typing import Union


# Util func to bypass hex() returning 3-digit numbers (e.g. 0x0 instead of 0x00). Needed for conversion to bytes datatype
def two_digit_hex_str(number: int):
    res = str(hex(number))
    if len(res) == 4:
        return res
    elif len(res) == 3:
        return "0x0" + res[2:]
    else:
        ValueError(f"Something is very wrong with this number: {res}. Occurred when trying to convert {number}")


def binary_dump_to_hex(path: str) -> pd.DataFrame:
    dump = pd.read_csv(path)
    dump["Channel 2"] = pd.to_numeric(dump["Channel 2"], errors='raise').astype('Int32')

    time = []
    miso = []
    mosi = []

    bit_counter = 0
    miso_bits = str()
    mosi_bits = str()

    for _, row in dump.iterrows():
        # print(bit_counter, row["Channel 2"], (bit_counter < 8 and row['Channel 2'] == 1))
        if bit_counter < 8 and row['Channel 2'] == 1:
            miso_bits = miso_bits + str(int(row['Channel 0']))
            mosi_bits = mosi_bits + str(int(row['Channel 1']))
            # print("added some bits:", row["Channel 0"], row["Channel 1"], miso_bits, mosi_bits)
            bit_counter += 1

            if bit_counter == 1:
                time.append(row['Time [s]'])
                continue
        # print("MISO:", miso_bits, "MOSI:", mosi_bits)

        if bit_counter == 8:
            miso.append(two_digit_hex_str(int(miso_bits, 2)))
            mosi.append(two_digit_hex_str(int(mosi_bits, 2)))
            miso_bits = ""
            mosi_bits = ""
            bit_counter = 0

    dump_dict = {
        "time": time,
        "MISO": miso,
        "MOSI": mosi
    }

    return pd.DataFrame(dump_dict)


def check_crc(data: Union[str, bytes], received_crc: hex) -> bool:
    if isinstance(data, str):
        data = bytes.fromhex(data)

    # CRC-16-Modbus-Algorithmus verwenden
    crc16 = crcmod.predefined.Crc('modbus')
    # CRC-Wert für das Datenpaket berechnen
    crc16.update(data)
    calculated_crc = crc16.hexdigest()

    return calculated_crc == received_crc


def filter_hex_dump(df: pd.DataFrame) -> list:
    potential_writes = df[df["MOSI"].isin(["0x58", "0x59"])]
    # print("found", len(potential_writes), "potential writes")
    writes = []
    for index, row in potential_writes.iterrows():
        # TODO: determine the length of payload/params
        param_len = 4
        # wait for start token
        max_index = index + 50  # randomly assume that there is a max of 1024 bytes of noise before start token is sent
        start_token_loc = 0
        for i in range(index, max_index):
            try:
                current_mosi = df.loc[i]["MOSI"]
            except (ValueError, KeyError):
                break  # we exceeded the end of the dataframe
            if current_mosi == "0xfe":
                start_token_loc = i
                break
        if start_token_loc <= 0:
            continue
        payload_len = 512  # is it enough to just skip through n bytes or do we need to analyze when the transfer starts?
        payload_df = df.loc[start_token_loc + 1:start_token_loc + payload_len]
        # print("start token loc", start_token_loc, "crc loc:", (start_token_loc + payload_len + 1))
        payload = ""
        for _, x in payload_df.iterrows():
            payload += x["MOSI"].replace("0x", "")
        try:
            is_valid_crc = check_crc(payload, df.loc[start_token_loc + payload_len + 1]["MISO"])  # TODO: MOSI or MISO?
        except (ValueError, KeyError):
            continue
        is_valid_crc = (df.loc[start_token_loc + payload_len + 1]["MOSI"] == "0x00")  # TODO remove this once using not flat 0x00 as crc
        # print("is correct crc:", is_valid_crc)
        if is_valid_crc:
            writes.append(payload)
    return writes


if __name__ == "__main__":
    df = binary_dump_to_hex("in/spi_trace.csv")
    print(df)
    df.to_csv("out/a.csv")
    writes = filter_hex_dump(df)
    print("found", len(writes), "valid writes:", writes)
