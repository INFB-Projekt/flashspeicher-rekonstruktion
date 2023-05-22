import pandas
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
        ValueError(f"Something is very wrong with this nomba: {res}. Occurred when trying to convert {number}")


def binary_dump_to_hex(path: str) -> pandas.DataFrame:  # Attention: this method returns single digit hex as such: e.g. "0x00" is "0x0"
    dump = pandas.read_csv(path)

    time = []
    miso = []
    mosi = []

    bit_counter = 0
    miso_bits = str()
    mosi_bits = str()

    for _, row in dump.iterrows():
        if bit_counter < 8 and row['Channel 2'] == 1:
            miso_bits = miso_bits + str(int(row['Channel 0']))
            mosi_bits = mosi_bits + str(int(row['Channel 1']))
            bit_counter += 1

            if bit_counter == 1:
                time.append(row['Time [s]'])
                continue

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

    return pandas.DataFrame(dump_dict)


def check_crc(data: Union[str, bytes], received_crc: hex) -> bool:
    print("data", data, received_crc)
    if isinstance(data, str):
        data = bytes.fromhex(data)

    # CRC-16-Modbus-Algorithmus verwenden
    crc16 = crcmod.predefined.Crc('modbus')
    # CRC-Wert für das Datenpaket berechnen
    crc16.update(data)
    calculated_crc = crc16.hexdigest()

    return calculated_crc == received_crc


def filter_hex_dump(df: pandas.DataFrame) -> list:
    potential_writes = df[df["MISO"].isin(["0x58", "0x59"])]
    print("found", len(potential_writes), "potential writes")
    writes = []
    for index, row in potential_writes.iterrows():
        # TODO: determine the length of payload/params
        param_len = 4
        payload_len = 512
        payload_df = df.loc[index:index + payload_len + param_len - 1]
        payload = ""
        for _, x in payload_df.iterrows():
            payload += x["MOSI"].replace("0x", "")
        a = check_crc(payload, df.loc[index + payload_len + param_len]["MISO"])
        print("is correct crc:", a)
        if check_crc(payload, df.loc[index + payload_len + param_len]["MISO"]):
            writes.append(payload)
    return writes


if __name__ == "__main__":
    df = binary_dump_to_hex("in/example_dump.csv")
    writes = filter_hex_dump(df)
    print(writes)
