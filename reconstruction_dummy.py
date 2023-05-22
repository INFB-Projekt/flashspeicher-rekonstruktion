import mmap
import contextlib
import os
import csv
import datetime


reconstruktionPath = "E:\\Vmshare"
csvPath = "E:\\Vmshare\\CSV"
imageName = "sdCard.img"

f = open(os.path.join(reconstruktionPath, imageName), "r+b")
mm = mmap.mmap(f.fileno(), 0)

dateString = "18.05.2023"
timeString = "14:22:02"

dateObj = datetime.datetime.strptime(dateString, "%d.%m.%Y")
timeObj = datetime.datetime.strptime(timeString, "%H:%M:%S")
datetimeObj = datetime.datetime.combine(dateObj.date(), timeObj.time())
rekostructionTimestamp = int(datetimeObj.timestamp()) * 1000

#find correct csv file
targetTrace = ""
for trace in os.listdir("CSV"):
    traceTimestamp = int(trace[:-4])
    if(rekostructionTimestamp > traceTimestamp):
        targetTrace = trace
    else: break

#find correct row in csv file
targetRow = 0
with open(f"CSV\\{targetTrace}", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader) #TODO remember to delete (maybe)

    for row in reader:
        currentRowTimeStamp = int(targetTrace[:-4]) + float(row[0]) * 1000
        if(rekostructionTimestamp > currentRowTimeStamp):
            targetRow += 1           
        else:
            break
    print("Reconstructing until the following point:")
    print(datetime.datetime.fromtimestamp(currentRowTimeStamp / 1000))
    csvfile.close()
print("Target Trace: " + targetTrace)
print("Target Row: "+ targetRow)

#Main reconstruction function
def reconstruction(csvName, rowCount):
    with open(f'CSV\\{csvName}', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader) #TODO remember to delete (maybe)
        currentRow = 0
    
        for row in reader:
            if(row[1] == "0x58" and (rowCount == -1 or currentRow < rowCount)):
                mm.seek(int(row[2], 0))
                hex_bytes = bytes.fromhex(row[3][2:])
                mm.write(hex_bytes)
            else: 
                print(currentRow)
                break
            currentRow += 1
        csvfile.close()


#Either reconstruct everything in file or only until last row
for csvName in os.listdir("CSV"):
    if(targetTrace != csvName):
        reconstruction(csvName, -1)
    else:
        reconstruction(csvName, targetRow)
        break

f.close()
mm.close
