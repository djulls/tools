#/usr/bin/env python

import time
import datetime
import argparse


def date_to_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('date',help='Datetime to be converted (format: yyyy-mm-ddThh:mm:ss)')

    args = parser.parse_args()

    print date_to_timestamp(args.date)
