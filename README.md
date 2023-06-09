# flash memory reconstruction

## sd_card_image_generator.py
### Usage
#### Execute from command line:
````
python sd_card_image_generator.py --sd-card-path /path/to/sd/card --zip-file-path /path/to/archive.zip --shellscript-location /path/to/createImage.sh --image-path /path/to/sdCard.img
````
#### for further information run:
````
python sd_card_image_generator.py --help
````

## reconstruction_dummy.py
### Usage
#### Execute from command line:
````
python reconstruction_dummy.py --reconstruction-path E:\\Vmshare --csv-path E:\\Vmshare\\CSV --image-name sdCard
````
#### for further information run:
````
python reconstruction_dummy.py --help
````
## Tests
Run following command in the root directory: 
````
python -m pytest
````