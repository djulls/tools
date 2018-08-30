#/usr/bin/env python

import time
import datetime
import argparse


def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('timestamp',help='timestamp to be converted (type: int)',type=int)

    args = parser.parse_args()

    print timestamp_to_date(args.timestamp)
