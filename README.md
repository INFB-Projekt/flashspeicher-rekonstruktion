# flash memory reconstruction

## Prerequisites
* python 3
* pipenv installed ``pip install pipenv``
* virtual environment created with ``pipenv install``


## Usage
### trace_generator.py
This script genrates a dummy trace in binary and saves it in "resources/bin" as a csv.
#### Execute from command line:
````
python3 trace_generator.py
````

### trace_analysis_main.py
This script runs all necessary sub-scripts for filtering all type of write commands. Saves the filtered trace to "resources/filtered_trace".
When executing the script you can set multiple flags for some options.
* --logger_level [ERROR, INFO or DEBUG]: ERROR = no logs, INFO = basic info (default), DEBUG = ultimate info
* --hex: uses already converted hex files for analyzing, if this flag is not set it uses a trace in binary and converts it to hex
* --fname [filename]: Filename of trace which should be analyzed
#### Excecute from command line (example):
````
python3 trace_analysis_main.py --fname 2023-06-19T16_52_37S927.csv --hex --logger DEBUG
````

### sd_card_image_generator.py
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
This script offers a convenient and efficient way to reconstruct data given a SD-Card image and a folder of CSV trace files based on a user-specified timestamp.
#### Execute from command line:
````
python trace_reconstruction.py --image-path /path/to/.img-file --csv-path path/to/csv --date DD.MM.YYYY --time HH:MM:SS
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