#!/usr/bin/env python3

import time
from datetime import datetime
import argparse
import requests
from requests.exceptions import ConnectionError, ReadTimeout, MissingSchema
from http import HTTPStatus
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-url', help = 'URL to analyse for redirects', required = True)
parser.add_argument('-w', help = 'Seconds to wait before retry', default=30)
args = parser.parse_args()

url = args.url
wait = int(args.w)

connected = False

while not connected:
    try:
        print('Trying to connect')
        print('Time: %s' % (datetime.now()))
        print('Domain: %s' % (url))
        r = requests.get(url, timeout = 15)
        connected = True
    except ReadTimeout as e:
        print('***** Read Timed Out *****')
        print('Trying again in %d seconds' % (wait))
        print('*' * 60)
        time.sleep(wait)
    except ConnectionError as e:
        print('***** Connection Error *****')
        print('Trying again in %d seconds' % (wait))
        print('*' * 60)
        time.sleep(wait)
    except MissingSchema as e:
        print('***** Missing Schema *****')
        print(e)
        print('Exiting')
        sys.exit(1)


statuscode = r.status_code
print('Successfully connected')
print('Status code: %d - %s' % (statuscode, HTTPStatus(statuscode).phrase))
