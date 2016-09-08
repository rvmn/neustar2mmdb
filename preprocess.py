#!/usr/bin/env python2.7

# This source code is subject to the terms of the MIT License. If a
# copy of the MIT License was not distributed with this file, you can
# obtain one at http://opensource.org/licenses/MIT.

from __future__ import absolute_import, division, print_function
import argparse
import cStringIO
import csv
import fileinput
import sys

import netaddr


'''klady@klady:/data/neustar $ head v727.281_24.50_20150320.csv
"start_ip_int","end_ip_int","country_code","country","state","city","latitude","longitude","time_zone"'''


def process_row(row, fields):
    res = []
    netblocks = netaddr.iprange_to_cidrs(netaddr.IPAddress(row['start_ip_int']), netaddr.IPAddress(row['end_ip_int']))
    for netblock in netblocks:
        row['netblock'] = netblock
        res.append([row[field] for field in fields])

    return res


def all_fields_null(row, fields):
    for field in fields:
        try:
            if row[field] != '':
                return False
        except KeyError:
            pass
    return True


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--fields', type=lambda x: x.split(','), default=('netblock', 'proxy_type', 'proxy_level'),
            help='comma-only (no spaces) separated list of the fields that you want in the output mmdb file')
    parser.add_argument('neustar_file', help='Neustar GeoPoint CSV file; use - to read from stdin')
    args = parser.parse_args(argv[1:])

    r = csv.DictReader(fileinput.input(args.neustar_file))
    w = csv.writer(sys.stdout)

    fields = args.fields

    w.writerow(fields)

    for row in r:
        if all_fields_null(row, fields):
            continue
        for res in process_row(row, fields):
            w.writerow(res)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
