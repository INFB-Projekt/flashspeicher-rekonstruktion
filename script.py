import os
import time
import shutil 
import subprocess
from zipfile import ZipFile

#change this to match the correct path to the sd card
pathToSdCard = "/home/lars/Downloads"
#path where the zipped images should be stored (including archive name)
zipPath = "/home/lars/Downloads/archive.zip"
#change this to point to the shell script
shellscriptLocation = "~/Desktop/createImage.sh"
#path where the images are created with the shell script (including name of image)
pathToImage = "/home/lars/Dokumente/sdCard.img"

file_name = "example.txt"
dir_name = "/testDirectory"

#delay in seconds (float)
delay = 2
#create image (yes / no)
shouldCreateImage = "yes"


counter = 0

def createFileAndWrite(string):
    with open(os.path.join(pathToSdCard, file_name), "w") as f:
        f.write(string)
        f.close()
    time.sleep(delay)
    createImage()

def createFileAndRead(string):
    with open(os.path.join(pathToSdCard, file_name), "w+") as f:
        f.write(string)
        f.seek(0)
        time.sleep(delay)
        f.read(10)
        f.close()
    time.sleep(delay)
    createImage()

def createImage():
    global counter
    if shouldCreateImage == "yes":
        print(f"Creating image {counter}...")
        process = subprocess.Popen(shellscriptLocation, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print("Done, zipping image...")
        zipFile.write(pathToImage, arcname=f"image{counter}.img")
        counter += 1
        print("Done")
    



if shouldCreateImage == "yes":
    zipFile = ZipFile(zipPath, 'w')

createFileAndWrite("A")
createFileAndWrite(10 * "A")
createFileAndWrite("ABCDEFGHIJ")
createFileAndWrite(10000 * "A\n")
createFileAndWrite(10000 * "A")

createFileAndRead(10 * "A")
createFileAndRead("ABCDEFGHIJ")

#creating folder and moving txt file into it
os.mkdir(pathToSdCard + dir_name)
shutil.move(pathToSdCard + "/" + file_name, pathToSdCard + dir_name) 
time.sleep(delay)
createImage()

#renaming file
os.rename(pathToSdCard + dir_name + "/" + file_name, pathToSdCard + dir_name + "/renamedFile.txt")
time.sleep(delay)
createImage()

#cleanup
os.remove(pathToSdCard + dir_name + "/renamedFile.txt")
os.rmdir(pathToSdCard + dir_name)
if shouldCreateImage == "yes":
    zipFile.close()
