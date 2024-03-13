# Description

This script uses REST api of a range of online geocoders. Some of them require a registration and the use of a private key to start geocoding, others don't.

You can store your key in a text file and pass it to the script.

# Example 

`python geocoding.py --help`  displays options

`python geocoding.py --api-key ../params/tomtom-api-key.txt --fun geocode --check --columns_map city localite country pays housenumber norue postcode codpos street rue --infile ../mmust/beldam_menages_lxbg.csv --outfile ../mmust/beldam_menages_lxbg_gc.csv`

# Usage 

    usage: geocoding_v2.py [-h] [--func {test,geocode}]
                           [--api {osm,tomtom,bing,arcgis}] [--check]
                           [--infile INFILE] [--outfile OUTFILE]
                           [--columns_map [COLUMNS_MAP ...]] [--api_key API_KEY]
                           [--params PARAMS]
    
    Geocoding with REST API
    
    optional arguments:
      -h, --help            show this help message and exit
      --func {test,geocode}
                            choose test to check parameters or geocode
      --api {osm,tomtom,bing,arcgis}
                            choose the geocoding API to use
      --check               display default parameters
      --infile INFILE       csv input file
      --outfile OUTFILE     csv output file
      --columns_map [COLUMNS_MAP ...]
                            link keys with the columnnames: city mycitycolumn
                            country col2 housenumber col4 postcode CP street col3
      --api_key API_KEY     textfile location with API-key
      --params PARAMS       read parameter file

You can save and overwrite the defaults parameters in a `PARAMS` textfile as follows :

    api: tomtom
    api_key: ../path/to/key_textfile.txt
    columns_map:city column_of_cityname