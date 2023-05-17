import time
import random

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


def create_csv(count):
    # get timestamp
    timestamp = current_milli_time()
    # create file
    with open(f".\output\{timestamp}.csv", "w") as f:
        # write header
        f.write("time;opcode;param;payload\n")
        # write body
        for i in range(count):
            line = f"{(i + 1) / 1000};0x58;{create_adress()};{create_payload_sw()}\n"
            f.write(line)



if __name__ == "__main__":
    count = int(input("Anzahl der Einträge: "))
    print("Create CSV...")
    create_csv(count)
    print("Done")


