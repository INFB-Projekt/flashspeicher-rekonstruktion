import time
import random
import csv
import pathlib

def current_milli_time():
    return round(time.time() * 1000)

def format_hex(digit, hex_num):
    # cut 0x from hex_num
    hex_num = str(hex_num)[2:].upper()
    # dif of digit and len of hex_num
    dif = digit - len(hex_num)
    zeros = "0" * dif
    return "0x" + zeros + hex_num


def create_adress():
    # max value 4 Bytes -> 32 bits -> 2^32 - 1
    max_value = 2**32 - 1
    # create a random adress
    adress = hex(random.randint(0, max_value))
    return format_hex(8, adress)


def create_payload_sw():
    # max value 512 Bytes -> 4096 bits -> 2^4096 - 1
    max_value = 2**4096 - 1
    # create a random payload for single write
    payload = hex(random.randint(0, max_value))
    return format_hex(1024, payload)

def calculate_crc(payload) -> str:
    crc8_func = crcmod.predefined.mkPredefinedCrcFun('crc-8')
    # Entferne das "0x" am Anfang, falls vorhanden
    if payload.startswith("0x"):
        payload = payload[2:]
    message = bytearray.fromhex(payload)
    crc = crc8_func(message)
    # Konvertiere den CRC-Wert in hexadezimale Wert
    crc_hex = hex(crc)[2:].zfill(2)
    return crc_hex.upper()

def create_csv(count):
    # get timestamp
    timestamp = current_milli_time()
    # get script directory
    script_dir = pathlib.Path().resolve()
    
    output_file = script_dir / f"{timestamp}.csv"

    # create file
    with open(output_file, "w", newline="") as f:
        # create csv writer
        writer = csv.writer(f, delimiter=";")
        # write header
        writer.writerow(["time", "opcode", "param", "payload"])
        # write body
        for i in range(count):
            time_val = (i + 1) / 1000
            opcode = "0x58"
            address = create_adress()
            payload = create_payload_sw()
            crc = calculate_crc(payload)
            writer.writerow([time_val, opcode, address, payload+crc])



if __name__ == "__main__":
    count = int(input("Anzahl der Einträge: "))
    print("Create CSV...")
    create_csv(count)
    print("Done")


