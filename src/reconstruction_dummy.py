import mmap
import os
import csv
import datetime
import argparse


def process_arguments():

    global image_path, csv_path, reconstruction_timestamp
    parser = argparse.ArgumentParser(description="Script to reconstruct data from a CSV file ")
    parser.add_argument("--image-path", required=True, help="Path to image file")
    parser.add_argument("--csv-path", required=True, help="Path to folder containing CSV files")
    parser.add_argument("--date", required=True, help="date in dd.mm.yyyy")
    parser.add_argument("--time", required=True, help="time in hh:mm:ss")
    args = parser.parse_args()
    image_path = args.image_path
    csv_path = args.csv_path
    date_string = args.date
    time_string = args.time

    date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
    time_obj = datetime.datetime.strptime(time_string, "%H:%M:%S")
    datetime_obj = datetime.datetime.combine(date_obj.date(), time_obj.time())
    reconstruction_timestamp = int(datetime_obj.timestamp()) * 1000


#find correct csv file
def find_csv_file(csv_name_list):
    global reconstruction_timestamp

    target_csv = ""
    if(reconstruction_timestamp < int(csv_name_list[0][:-4])):
        raise Exception("Timestamp too early to reconstruct")
    for trace in csv_name_list:
        trace_timestamp = int(trace[:-4])
        if(reconstruction_timestamp > trace_timestamp):
            target_csv = trace
        else: break
    return target_csv

#find correct row in csv file
def find_target_row(target_csv, path_dest_csv):
    target_row = 0
    with open(path_dest_csv, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) #skip the first line in each CSV file

        if(reconstruction_timestamp < int(target_csv[:-4])):
            raise Exception("Timestamp too early")

        for row in reader:
            current_row_timestamp = int(target_csv[:-4]) + float(row[0]) * 1000
            if(reconstruction_timestamp > current_row_timestamp):
                target_row += 1           
            else:
                break
        print("Reconstructing until the following point:")
        print(datetime.datetime.fromtimestamp(current_row_timestamp / 1000))
        csvfile.close()
    print("Target Trace: " + str(target_csv))
    print("Target Row: "+ str(target_row))
    return target_row

#Main reconstruction function
def reconstruction(row_count, path_dest_csv):
    f = open(image_path, "r+b")
    mm = mmap.mmap(f.fileno(), 0)

    with open(path_dest_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) #skip the first line in each CSV file
        current_row = 0
    
        for row in reader:
            if(row[1] == "0x58" and (row_count == -1 or current_row < row_count)):
                mm.seek(int(row[2], 0))
                hex_bytes = bytes.fromhex(row[3][2:])
                mm.write(hex_bytes)
            else: 
                print(current_row)
                break
            current_row += 1
        csvfile.close()
    
    f.close()
    mm.close()


if __name__ == "__main__":
    image_path = ""
    csv_path = ""

    process_arguments()
    target_csv = find_csv_file(os.listdir(csv_path))

    target_row = find_target_row(target_csv, f"{csv_path}/{target_csv}")

    #Either reconstruct everything in file or only until last row
    for csv_name in os.listdir(csv_path):
        if(target_csv != csv_name):
            reconstruction(-1, f'{csv_path}/{csv_name}')
        else:
            reconstruction(target_row, f'{csv_path}/{csv_name}')
            break

