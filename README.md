# Description

This script uses [REST api](https://fr.wikipedia.org/wiki/Representational_state_transfer) of a range of online geocoders. Some of them require a registration and the use of a private key to start geocoding, others don't.

You can store your key in a text file and pass it to the script.

The supported services are : tomtom, OpenStreetMap, Bing and arcgis but this script can easily be extented to any provider supported by the python geocoder. See the provider list  
[here](https://github.com/DenisCarriere/geocoder?tab=readme-ov-file#providers).



# Example 

`python geocoding.py --help`  displays options

Run the geocoder on the sample.csv dataset:

`python geocoding.py --check --api_key ../params/tomtom-api-key.txt --params ../params/geocoding.conf --func geocode`

# Usage 

    usage: geocoding.py [-h] [--func {test,geocode}]
                        [--api {osm,tomtom,bing,arcgis}] [--check]
                        [--infile INFILE] [--outfile OUTFILE]
                        [--columns_map KEY1:VAL1,KEY2:VAL2...] [--api_key API_KEY]
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
      --columns_map KEY1:VAL1,KEY2:VAL2...
                            link keys with the columnnames: city:mycitycolumn,coun
                            try:col2,housenumber:col4,postcode:CP,street:col3
      --api_key API_KEY     textfile location with API-key
      --params PARAMS       read parameter file

You can save and overwrite the defaults parameters in a `PARAMS` textfile as follows :

    # comment line
    api = tomtom
    api_key = ../path/to/key_textfile.txt
    columns_map = city:ville,country:pays,housenumber:numéro,postcode:CP,street:rue

If you use the parameter `columns_map`, every key **must** be provided in the columns_map with an existing column of your input file.
Whatever other columns existing in the csv file will be preserved in the output file.  

The results returned by the online geocoder will be stored in new columns:
`to_geocode,gc_lat,gc_lon,gc_address,gc_country,gc_postcode,gc_city`

The coordinate system used is WGS 84 (epsg:4326).

# Requirements


