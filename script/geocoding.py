import re

import pandas as pd
import geocoder
import numpy as np
import argparse
import urllib
import sys
from time import sleep

infile = '../data/1_dataset/sample.csv'
outfile = '../data/1_dataset/geocode.csv'
defaultcolnames = {'city': 'citycolumnname', 'country': 'country', 'housenumber': 'housenumber', 'postcode': 'postcode', 'street': 'street'}
# countryset = ['LU','FR','DE','BE']

'''
    This is the refactored version of the geocoding function


'''


def geocode(args):
    '''
        infile : csv file with the following columns 'id', 'city', 'country', 'housenumber', 'postcode', 'street'

    '''
    # geocoding columns
    # countryset = args.countryset

    if args.infile:
        infile = args.infile

    if args.outfile:
        outfile = args.outfile

    d = defaultcolnames
    if args.columns_map:
        columns_map = args.columns_map
        if not isinstance(columns_map, dict):
            i = iter(columns_map)
            columns_map = dict(zip(i, i))
        d = columns_map

    df = pd.read_csv(infile)

    df.fillna('', inplace=True)

    df['hnum_street'] = df.apply(lambda x: ' '.join([str(x[i]) for i in [d['housenumber'], d['street']] if x[d['street']] != '']), axis=1)

    df['to_geocode'] = df.apply(lambda x: ', '.join([str(x[i]) for i in ['hnum_street', d['postcode'], d['city'], d['country']] if x[i] != '']), axis=1)
    df['to_geocode'] = df['to_geocode'] + '|' + df[d['country']]
    df.loc[(df['hnum_street'] == '') & (df[d['city']] == '') & (df[d['postcode']] == ''), 'to_geocode'] = ''
    dfg = df.loc[(df["to_geocode"].notna()) & (df["to_geocode"] != ''), :].copy()

    def tomtom_geocode_line2(y):
        sleep(1)
        country = y.split('|')[1]
        x = urllib.parse.quote(y.split('|')[0], safe='')
        print(x)
        g = geocoder.tomtom(x, key=getApiKey(args), countrySet=country)
        coords = [np.nan, np.nan, '', '', '', '']
        if g.status == 'OK':
            coords = g.latlng + [g.address, g.country, g.postal, g.city]
            print([(r.address, r.country, r.latlng) for r in g])
        else:
            print('no results for this')
        return coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]

    def bing_geocode_line2(y):
        sleep(1)
        country = y.split('|')[1]
        x = y.split('|')[0]
        print(x)
        g = geocoder.bing(x, key=getApiKey(args), countrySet=country)
        coords = [np.nan, np.nan, '', '', '', '']
        if g.status == 'OK':
            coords = g.latlng + [g.address, g.country, g.postal, g.city]
            print([(r.address, r.country, r.latlng) for r in g])
        else:
            print('no results for this')
        return coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]

    def osm_geocode_line2(y):
        sleep(1)
        country = y.split('|')[1]
        x = y.split('|')[0]
        print(x)
        g = geocoder.osm(x, countrySet=country)
        coords = [np.nan, np.nan, '', '', '', '']
        if g.status == 'OK':
            coords = g.latlng + [g.address, g.country, g.postal, g.city]
            print([(r.address, r.country, r.latlng) for r in g])
        else:
            print('no results for this')
        return coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]

    def arcgis_geocode_line2(y):
        sleep(1)
        country = y.split('|')[1]
        x = urllib.parse.quote(y.split('|')[0], safe='')
        print(x)
        g = geocoder.arcgis(x, countrySet=country)
        coords = [np.nan, np.nan, '', '', '', '']
        if g.status == 'OK':
            coords = g.latlng + [g.address, g.country, g.postal, g.city]
            print([(r.address, r.country, r.latlng) for r in g])
        else:
            print('no results for this')
        return coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]

    if args.api == 'osm':
        dfg['gc_lat'], dfg['gc_lon'], dfg['gc_address'], dfg['gc_country'], \
        dfg['gc_postcode'], dfg['gc_city'] = zip(*dfg['to_geocode'].map(osm_geocode_line2))
    elif args.api == 'tomtom':
        dfg['gc_lat'], dfg['gc_lon'], dfg['gc_address'], dfg['gc_country'], \
        dfg['gc_postcode'], dfg['gc_city'] = zip(*dfg['to_geocode'].map(tomtom_geocode_line2))
    elif args.api == 'bing':
        dfg['gc_lat'], dfg['gc_lon'], dfg['gc_address'], dfg['gc_country'], \
        dfg['gc_postcode'], dfg['gc_city'] = zip(*dfg['to_geocode'].map(bing_geocode_line2))
    elif args.api == 'arcgis':
        dfg['gc_lat'], dfg['gc_lon'], dfg['gc_address'], dfg['gc_country'], \
        dfg['gc_postcode'], dfg['gc_city'] = zip(*dfg['to_geocode'].map(arcgis_geocode_line2))

    dfg.to_csv(outfile, index=False)
    print('geocoding done')


def getApiKey(args):
    """
        Read a text key file in args.key with the key for the API

        Arguments
        ---------
            args    : from argparse
        Returns
        -------
            string with the key
    """
    data = ''
    try:
        with open(f'{args.api_key}', 'r') as file:
            data = file.read().replace('\n', '')
    except Exception as err:
        print(f'Error occurred: {err}')
    return data


def test(args):
    check(args)
    print('test done. use "--func geocode" to start the geocoding')


def check(args):
    print('check arguments')
    for key in vars(args).keys():
        print(f'\t{key} : {vars(args)[key]}')


class StoreDictKeyPair(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        for kv in values.split(","):
            k, v = kv.split(":")
            my_dict[k] = v
        setattr(namespace, self.dest, my_dict)


class LoadFromFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            r = re.split('\n', f.read())  # split text with lines
            r = [k.strip() for k in r if not (k.startswith("#") or k == "")]  # exclude comments or empty lines
            j = "\n".join(["--" + j for j in r])  # adds the first -- indicating the parameter's name
            delimiters = "=\n"  # The delimiters to split the parameters on
            # Create a regular expression pattern from the delimiters
            pattern = "|".join(map(re.escape, delimiters))
            r = [k.strip() for k in re.split(pattern, j) if not (k == "")]  # Split the string using the pattern and parse arguments in the list excluding empty elements
            parser.parse_args(r, namespace)  # store them in the target namespace


def main():
    apikey = './my/tomtom-api-key.txt'
    parser = argparse.ArgumentParser(description=f'Geocoding with REST API')
    parser.add_argument('--func', help='choose test to check parameters or geocode', default='test', choices=['test', 'geocode'])
    parser.add_argument('--api', help='choose the geocoding API to use', choices=['osm', 'tomtom', 'bing', 'arcgis'], default='arcgis')
    parser.add_argument('--check', help='display default parameters', action="store_true")
    parser.add_argument('--infile', help='csv input file', default='../data/sample.csv')
    parser.add_argument('--outfile', help='csv output file', default='../data/sample_geocoded.csv')
    # parser.add_argument('--columns_map', help='link keys with the columnnames: city mycitycolumn country col2 housenumber col4 postcode CP street col3',
    #                     nargs='*', required=False,
    #                     default=defaultcolnames)
    parser.add_argument("--columns_map", dest="columns_map", help='link keys with the columnnames: city:mycitycolumn,country:col2,housenumber:col4,postcode:CP,street:col3',
                        action=StoreDictKeyPair, metavar="KEY1:VAL1,KEY2:VAL2...", required=False,
                        default=defaultcolnames)
    parser.add_argument('--api_key', help='textfile location with API-key', required=False, default=apikey)
    parser.add_argument('--params', type=open, action=LoadFromFile, help="read parameter file", required=False)
    # parser.add_argument('--countryset', help='Country set to which restrict the results', nargs='*', required=False, default=countryset)

    parser.set_defaults(func='test')
    args = parser.parse_args()

    if args.func == 'test':
        test(args)
    elif args.func == 'geocode':
        if args.check:
            check(args)
        geocode(args)


if __name__ == "__main__":
    sys.exit(main())