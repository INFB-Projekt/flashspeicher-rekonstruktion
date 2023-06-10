# flash memory reconstruction

## Prerequisites
* python 3.10
* pipenv installed ``pip install pipenv``
* virtual environment created with ``pipenv install``


## Usage
### sd_card_image_generator.py
#### Execute from command line:
````
python sd_card_image_generator.py --sd-card-path /path/to/sd/card --zip-file-path /path/to/archive.zip --shellscript-location /path/to/createImage.sh --image-path /path/to/sdCard.img
````
#### for further information run:
````
python sd_card_image_generator.py --help
````

### reconstruction_dummy.py
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
pytest
````