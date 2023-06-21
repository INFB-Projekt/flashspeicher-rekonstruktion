# flash memory reconstruction

## Prerequisites
* python 3
* pipenv installed ``pip install pipenv``
* virtual environment created with ``pipenv install``


## Usage
### shellscript_sd_card_to_img.sh
#### Description:
This shell script can create an image of any storage device on Linux.
Make sure to change the variables in the script itself.
#### Execute from command line:
````
./shellscript_sd_card_to_img.sh
````
### sd_card_image_generator.py
#### Description:
This script creates and writes to a text file. It can also optionally automatically create a image after each step. It is used to easily create a predictable trace for testing purposes.
#### Execute from command line:
````
python sd_card_image_generator.py --sd-card-path /path/to/sd/card --zip-file-path /path/to/archive.zip --shellscript-location /path/to/createImage.sh --image-path /path/to/sdCard.img
````
#### for further information run:
````
python sd_card_image_generator.py --help
````

### trace_reconstruction.py
#### Description:
This script offers a convenient and efficient way to reconstruct data given a SD-Card image and a folder of CSV trace files based on a user-specified timestamp.
#### Execute from command line:
````
python trace_reconstruction.py --image-path E:\Vmshare\sdCard.img --csv-path E:\Vmshare\CSV --date 18.05.2023 --time 14:22:02
````
#### for further information run:
````
python trace_reconstruction.py --help
````
## Tests
#### Execute from command line: 
````
pytest
````