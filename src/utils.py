# bypass hex() returning 3-digit numbers (e.g. 0x0 instead of 0x00). Needed for conversion to bytes datatype
def two_digit_hex_str(number: int):
    res = str(hex(number))
    if len(res) == 4:
        return res
    elif len(res) == 3:
        return "0x0" + res[2:]
    else:
        ValueError(f"Something is very wrong with this number: {res}. Occurred when trying to convert {number}")


def concat_df_key_to_hex(df, key):
    """Helper function to transform the two digit hex numbers all starting with 0x of dump dataframe into one hex"""
    hex = ""
    for _, x in df.iterrows():
        hex += x[key][2:]
    return hex
