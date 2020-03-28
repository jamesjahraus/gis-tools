"""
lookouts.py

This module is used to generate a csv file of a state's lookout towers by scraping http://nhlr.org/lookouts/.

google/python-fire is used to turn each function call into a CLI.

see: https://github.com/google/python-fire/blob/master/docs/guide.md

To run call make_lookout_csv(state, debug='INFO')

Example:

states: [AZ, CA, CO, ID, MT, NM, NV, OR, UT, WA, WY]

> python lookouts.py make_lookout_csv UT

:return: UT_lookout.csv

(NAME, REGNUM, STATE, LATITUDE, LONGITUDE,
 ELEVATION, ADMIN, IMAGE, DESC, T_HEIGHT, A_STAFFED)

:author: James Jahraus
"""

import os
import sys
import logging
import fire
import requests
from bs4 import BeautifulSoup
import csv
import helpers

logger = logging.getLogger(__name__)


def write_csv(state, lookouts):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    # Output .csv file
    file_name = '{0}_lookouts.csv'.format(state)
    csv_path = os.path.join(sys.path[0], file_name)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'NAME', 'URL', 'GOOGLEMAP', 'REGNUM', 'STATE', 'LATITUDE',
            'LONGITUDE', 'ELEVATION', 'ADMIN', 'DESC', 'T_HEIGHT', 'A_STAFFED'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lookout in lookouts:
            writer.writerow(lookout)


def get_soup(url):
    """GETs a html BeautifulSoup object.

    :param url: URL for a html page to be parsed.
    """

    with requests.Session() as s:
        response = s.get(url)
        logger.debug('HTTP GET PAGE RESPONSE: {0} - {1}'.format(
            response.status_code, response.text))
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_lookout(url):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    logger.info('LOOKOUT URL IS: {}'.format(url))
    soup = get_soup(url)
    search_strings = [
        'Registry Numbers', 'Coordinates', 'Elevation', 'Administered by',
        'Description'
    ]
    lookout_values = []

    for find in search_strings:
        if soup.find(text=find) == find:
            logger.debug('FIND: {0}'.format(soup.find(text=find)))
            lookout_value = soup.find(text=find).parent.find_next_siblings()
            lookout_text = lookout_value[0].text.strip()
            lookout_text = lookout_text.replace(',', '')
            lookout_text = lookout_text.replace('(', '')
            lookout_text = lookout_text.replace(')', '')
            lookout_values.append(lookout_text)
        else:
            logger.debug('FIND: {0} {1}'.format('did not find', find))
            lookout_values.append('NODATA')

    keys = ['regnum', 'coordinates', 'elevation', 'admin', 'desc']
    lookout_dict = dict(zip(keys, lookout_values))
    logger.debug('lookout_dict: {}'.format(lookout_dict))
    return lookout_dict


def get_lookout_urls(state):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    host = 'http://nhlr.org'
    url = '{0}/lookouts/us/{1}'.format(host, state)
    logger.debug('URL IS: {}'.format(url))
    soup = get_soup(url)
    table = soup.table
    table_rows = table.find_all('td')
    logger.debug('table_rows: {}'.format(table_rows))
    lookout_urls = []
    for row in table_rows:
        if row.find_all('a'):
            logger.debug('link row: {}'.format(row))
            name = row.get_text()
            logger.debug('name: {}'.format(name))
            for a in row.find_all('a', href=True):
                logger.debug('a: {}'.format(a['href']))
                lookout = '{0}{1}'.format(host, a['href'])
            lookout_urls.append((name, lookout))
        else:
            logger.debug('junk row: {}'.format(row))
    logger.debug('lookout_urls: {}'.format(lookout_urls))
    return lookout_urls


def fix_regnum(regnum):
    regnum = regnum.split('view')[0].strip()
    logger.debug('value: {}'.format(regnum))
    return regnum


def fix_coordinates(coordinates):
    coordinates = coordinates.split('\n')[2].strip()
    coordinates = coordinates.split('° ')
    lat = coordinates[0].replace('°', '').strip()
    lon = coordinates[1].replace('°', '').strip()
    if lat[0] == 'S':
        lat = '{0}{1}'.format('-', lat[1:].strip())
    else:
        lat = lat[1:].strip()
    if lon[0] == 'W':
        lon = '{0}{1}'.format('-', lon[1:].strip())
    else:
        lon = lon[1:].strip()
    logger.debug('value: {}'.format(lon))
    return lat, lon


def fix_elevation(elevation):
    elevation = elevation.split('ft')[0].strip()
    return elevation


def format_lookout_raw(lookout_raw):
    values = []
    values.append(fix_regnum(lookout_raw['regnum']))
    coordinates = fix_coordinates(lookout_raw['coordinates'])
    values.append(coordinates[0])
    values.append(coordinates[1])
    values.append(fix_elevation(lookout_raw['elevation']))
    values.append(lookout_raw['admin'].strip())
    values.append(lookout_raw['desc'].strip())
    logger.debug('values: {}'.format(values))
    keys = ['regnum', 'lat', 'lon', 'elevation', 'admin', 'desc']
    lookout_data = 'test'
    lookout_data = dict(zip(keys, values))
    return lookout_data


def make_lookout_dict(state, name, url):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    keys = [
        'NAME', 'URL', 'GOOGLEMAP', 'REGNUM', 'STATE', 'LATITUDE', 'LONGITUDE',
        'ELEVATION', 'ADMIN', 'DESC', 'T_HEIGHT', 'A_STAFFED'
    ]
    lookout_dict = {k: None for k in keys}
    lookout_dict['NAME'] = name
    lookout_dict['URL'] = url
    lookout_dict['STATE'] = state
    lookout_raw = get_lookout(url)
    logger.debug('lookout raw: {}'.format(lookout_raw))
    lookout_data = format_lookout_raw(lookout_raw)
    lookout_dict[
        'GOOGLEMAP'] = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(
            lookout_data['lat'], lookout_data['lon'])
    lookout_dict['REGNUM'] = lookout_data['regnum']
    lookout_dict['LATITUDE'] = lookout_data['lat']
    lookout_dict['LONGITUDE'] = lookout_data['lon']
    lookout_dict['ELEVATION'] = lookout_data['elevation']
    lookout_dict['ADMIN'] = lookout_data['admin']
    lookout_dict['DESC'] = lookout_data['desc']
    logger.debug('lookout dict: {}'.format(lookout_dict))
    return lookout_dict


def make_lookouts(state, lookout_urls):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    lookouts = []
    for name, url in lookout_urls:
        lookout_dict = make_lookout_dict(state, name, url)
        lookouts.append(lookout_dict)
    return lookouts


def make_lookout_csv(state, debug='INFO'):
    """Desc.

    :param 1: asdf.
    :return: asdf.
    """

    helpers.setup_logging(level=debug)
    logger.info('STATE IS: {}'.format(state))
    lookout_urls = get_lookout_urls(state)
    logger.debug('LOOKOUT URLS: {}'.format(lookout_urls))
    lookouts = make_lookouts(state, lookout_urls)
    write_csv(state, lookouts)


if __name__ == '__main__':
    fire.Fire()
