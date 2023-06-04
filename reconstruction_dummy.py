import mmap
import os
import csv
import datetime
import argparse


parser = argparse.ArgumentParser(description="Script to reconstruct data from a CSV file ")
parser.add_argument("--reconstruction-path", required=True, help="Path to the desired destination")
parser.add_argument("--csv-path", required=True, help="Path to the csv file")
parser.add_argument("--image-name", required=True, help="Name of the image")
args = parser.parse_args()
reconstruction_path = args.reconstruction_path
csv_path = args.csv_path
image_name = args.image_name


f = open(os.path.join(reconstruction_path, image_name), "r+b")
mm = mmap.mmap(f.fileno(), 0)


date_string = "18.05.2023"
time_string = "14:22:02"

date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
time_obj = datetime.datetime.strptime(time_string, "%H:%M:%S")
datetime_obj = datetime.datetime.combine(date_obj.date(), time_obj.time())
rekostruction_timestamp = int(datetime_obj.timestamp()) * 1000

#find correct csv file
target_trace = ""
for trace in os.listdir("CSV"):
    trace_timestamp = int(trace[:-4])
    if(rekostruction_timestamp > trace_timestamp):
        target_trace = trace
    else: break

#find correct row in csv file
target_row = 0
with open(f"CSV\\{target_trace}", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader) #TODO remember to delete (maybe)

    for row in reader:
        current_row_timestamp = int(target_trace[:-4]) + float(row[0]) * 1000
        if(rekostruction_timestamp > current_row_timestamp):
            target_row += 1           
        else:
            break
    print("Reconstructing until the following point:")
    print(datetime.datetime.fromtimestamp(current_row_timestamp / 1000))
    csvfile.close()
print("Target Trace: " + target_trace)
print("Target Row: "+ target_row)

#Main reconstruction function
def reconstruction(csv_name, row_count):
    with open(f'CSV\\{csv_name}', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) #TODO remember to delete (maybe)
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


#Either reconstruct everything in file or only until last row
for csv_name in os.listdir("CSV"):
    if(target_trace != csv_name):
        reconstruction(csv_name, -1)
    else:
        reconstruction(csv_name, target_row)
        break

f.close()
mm.close

