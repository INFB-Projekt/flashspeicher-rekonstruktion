import pandas


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
            miso.append(hex(int(miso_bits, 2)))
            mosi.append(hex(int(mosi_bits, 2)))
            miso_bits = ""
            mosi_bits = ""
            bit_counter = 0

    dump_dict = {
        "time": time,
        "MISO": miso,
        "MOSI": mosi
    }

    return pandas.DataFrame(dump_dict)


def filter_hex_dump(df: pandas.DataFrame) -> pandas.DataFrame:
    filtered_df = df[df["MISO"].isin(["0x58", "0x59"])]
    #aaa = df[df["MOSI"] == "0x00"]
    #print(aaa)
    writes = []
    for index, row in filtered_df.iterrows():
        writes.append([])
        for i in range(index, index + 512):
            writes[-1].append(df.loc[i])
            print(df.loc[i]["MISO"])
            if df.loc[i]["MISO"] == "0x0":
                print("break reached")
                break
    print(writes)
    return filtered_df


if __name__ == "__main__":
    df = binary_dump_to_hex("in/example_dump.csv")
    print(df)
    #df = filter_hex_dump(df)
    #print(df)
