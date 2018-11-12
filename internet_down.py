#!/usr/bin/env python

__doc__ = '''
Checks internet connectivity and gives the option of informing Comcast via
Twitter that internet is down.
'''

__copyright__ = '''
MIT License

Copyright (c) 2018 bandeezy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Author: Nick S.
# Username: bandeezy

import sys
from datetime import datetime
import time

from argparse import ArgumentParser

try:
    from modules.twitter_api import get_twitter_account_info
except ImportError:
    print("Could not import module 'twitter_api'. Ensure it exists within the\
           modules folder.")
    sys.exit(1)
try:
    from modules.csv_api import write_results_to_csv
except ImportError:
    print("Could not import module 'csv_api'. Ensure it exists within the\
           modules folder.")
    sys.exit(1)
try:
    from modules.internet_tools import connected_to_internet
except ImportError:
    print("Could not import module 'connected_to_internet'. Ensure it exists within the\
           modules folder.")
    sys.exit(1)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--enable_tweet', action='store_true', default=False)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    while True:
        if not connected_to_internet():
            start_time = datetime.now()
            while not connected_to_internet():
                pass  # do nothing
            end_time = datetime.now()
            time_diff = end_time - start_time

            ping = 0
            download = 0
            upload = 0
            # TODO: configure UTC time to either have T
            #       or remove T from the speedtest UTC time
            results_csv = ("NA,NA,NA," + str(datetime.utcnow()) + ",NA," +
                           str(ping) + "," + str(download) + "," + str(upload)
                           + "," + str(time_diff.seconds))

            write_results_to_csv(results_csv)

            if args.enable_tweet:
                t = get_twitter_account_info()
                tweet = ("Why has my internet been down for "
                         "{} seconds in ".format(time_diff.seconds) +
                         "Mountain View, CA? #comcastoutage "
                         "#xfinityoutage")
                t.update_status(status=tweet)
                print("Internet down tweet sent: " + tweet)
            else:
                print("Internet was down for {} ".format(time_diff.seconds) +
                      "seconds but tweet was not sent since argument was "
                      "not set")
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    main()
