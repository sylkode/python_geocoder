import pandas as pd
import geocoder
import numpy as np
import argparse
import urllib
import sys

infile = '../data/1_dataset/sample.csv'
outfile = '../data/1_dataset/geocode.csv'
defaultcolnames = {'city':'citycolumnname', 'country':'country', 'housenumber':'housenumber', 'postcode':'postcode', 'street':'street'}
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
        if not isinstance(columns_map,dict):
            i = iter(columns_map)
            columns_map = dict(zip(i, i))
        d = columns_map
    
    df = pd.read_csv(infile)

    df.fillna('', inplace=True)

    df['hnum_street'] = df.apply(lambda x: ' '.join([str(x[i]) for i in [d['housenumber'], d['street']] if x[d['street']] != '']), axis=1)

    df['to_geocode'] = df.apply(lambda x: ', '.join([str(x[i]) for i in ['hnum_street', d['postcode'],d['city'], d['country']] if x[i] != '']), axis=1)
    df.loc[(df['hnum_street']=='') & (df[d['city']]=='') & (df[d['postcode']]==''), 'to_geocode' ] = ''
    dfg = df.loc[(df["to_geocode"].notna()) & (df["to_geocode"]!=''),:].copy()
  
    def tomtom_geocode_line(x):
        x = urllib.parse.quote(x, safe='')
        print(x)
        g = geocoder.tomtom(x, key=getApiKey(args))
        coords = [np.nan,np.nan,'','','','']
        if g.status=='OK':
            coords = g.latlng +[ g.address, g.country, g.postal, g.city]
        return coords[0], coords[1], coords[2], coords[3], coords[4], coords[5]

    dfg['gc_lat'], dfg['gc_lon'], dfg['gc_address'], dfg['gc_country'], \
        dfg['gc_postcode'], dfg['gc_city'] = zip(*dfg['to_geocode'].map(tomtom_geocode_line))
    dfg.to_csv(outfile, index=False)

    
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
    data=''
    try:
        with open(f'{args.key}', 'r') as file:
            data = file.read().replace('\n', '')
    except Exception as err:
        print(f'Error occurred: {err}')
    return data

def test(args):
    print('test success')

def check(args):
    print('check arguments')
    for key in vars(args).keys():
        print(f'\t{key} : {vars(args)[key]}')

    
def main():
    apikey ='./my/tomtom-api-key.txt'
    parser = argparse.ArgumentParser(description=f'Geocoding with Tomtom REST API')
    parser.add_argument('--func', help='function to run', required=True, choices=['test','geocode'])
    parser.add_argument('--check', help='display default parameters', action="store_true")
    parser.add_argument('--infile', help='input file', default='../data/sample.csv')
    parser.add_argument('--outfile', help='output file', default='../data/sample_geocoded.csv')
    parser.add_argument('--columns_map', help='maps column names of the input file with the keys: city mycitycolumn country col2 housenumber col4 postcode CP street col3', nargs='*', required=False, default=defaultcolnames)
    parser.add_argument('--api-key', dest='key', help='API-key filename (textfile)', required=False, default=apikey)
    # parser.add_argument('--countryset', help='Country set to which restrict the results', nargs='*', required=False, default=countryset)
    
    parser.set_defaults(func='test')
    args = parser.parse_args()
    if args.check:
        check(args)
    if args.func == 'test':
        test(args)
    elif args.func == 'geocode':
        geocode(args)
    elif args.func == 'geocoding_precision':
        geocoding_precision(args)

if __name__ == "__main__":
    sys.exit(main())