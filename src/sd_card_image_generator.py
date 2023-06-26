import os
import time
import shutil 
import subprocess
import argparse
from zipfile import ZipFile

parser = argparse.ArgumentParser(description="Script to create SD card images and archive them")
parser.add_argument("--sd-card-path", required=True, help="Path to the SD card directory")
parser.add_argument("--zip-file-path", required=True, help="Path to the archive file")
parser.add_argument("--shellscript-location", required=True, help="Path to the shell script")
parser.add_argument("--image-path", required=True, help="Path to the SD card image")

args = parser.parse_args()

sd_card_path = args.sd_card_path
zip_file_path = args.zip_file_path
shellscript_location = args.shellscript_location
image_path = args.image_path

file_name = "example.txt"
dir_name = "/testDirectory"

#delay bin seconds (float)
delay = 2
#create image (yes / no)
should_create_image = "yes"


counter = 0

def createFileAndWrite(string):
    with open(os.path.join(sd_card_path, file_name), "w") as f:
        f.write(string)
    time.sleep(delay)
    createImage()

def createFileAndRead(string):
    with open(os.path.join(sd_card_path, file_name), "w+") as f:
        f.write(string)
        f.seek(0)
        time.sleep(delay)
        f.read(10)
    time.sleep(delay)
    createImage()

def createImage():
    global counter
    if should_create_image == "yes":
        print(f"Creating image {counter}...")
        process = subprocess.Popen(shellscript_location, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print("Done, zipping image...")
        zipFile.write(image_path, arcname=f"image{counter}.img")
        counter += 1
        print("Done")
    



if should_create_image == "yes":
    zipFile = ZipFile(zip_file_path, 'w')

createFileAndWrite("A")
createFileAndWrite(10 * "A")
createFileAndWrite("ABCDEFGHIJ")
createFileAndWrite(10000 * "A\n")
createFileAndWrite(10000 * "A")

createFileAndRead(10 * "A")
createFileAndRead("ABCDEFGHIJ")

#creating folder and moving txt file into it
os.mkdir(sd_card_path + dir_name)
shutil.move(sd_card_path + "/" + file_name, sd_card_path + dir_name) 
time.sleep(delay)
createImage()

#renaming file
os.rename(sd_card_path + dir_name + "/" + file_name, sd_card_path + dir_name + "/renamedFile.txt")
time.sleep(delay)
createImage()

#cleanup
os.remove(sd_card_path + dir_name + "/renamedFile.txt")
os.rmdir(sd_card_path + dir_name)
if should_create_image == "yes":
    zipFile.close()
