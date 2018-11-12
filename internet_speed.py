#!/usr/bin/env python2

__doc__ = '''
Checks internet speed and gives the option of informing Comcast via
Twitter that the internet connection is slow. Additionally, this records
internet speed data in CSV format for future plotting.
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

try:
    import speedtest
except ImportError:
    print("Could not import module 'speedtest'. Has it been installed?")
    sys.exit(1)
try:
    from modules.twitter_api import get_twitter_account_info
except ImportError:
    print("Could not import module 'twitter_api'. Ensure it exists within the "
          "modules folder.")
    sys.exit(1)
try:
    from modules.csv_api import write_results_to_csv
except ImportError:
    print("Could not import module 'csv_api'. Ensure it exists within the "
          "modules folder.")
    sys.exit(1)
try:
    from modules.internet_tools import (connected_to_internet,
                                        convert_bps_to_mbps)
except ImportError:
    print("Could not import module 'connected_to_internet'. Ensure it exists "
          "within the modules folder.")
    sys.exit(1)
try:
    from modules.common_argument_parser import parse_and_validate_arguments
except ImportError:
    print("Could not import module 'connected_to_internet'. Ensure it exists "
          "within the modules folder.")
    sys.exit(1)


def get_speedtest_data():
    print("Testing internet speed...")
    servers = []

    s = speedtest.Speedtest()
    s.get_servers(servers)
    # select server with lowest latency
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=False)

    return s.results


def main():
    args = parse_and_validate_arguments(__file__, __doc__, threshold=True)

    # TODO: clean up this syntax
    if not connected_to_internet():
        print('Not connected to the internet. Please connect to a network '
              'and try again.')
        return False

    results = get_speedtest_data()
    download = convert_bps_to_mbps(results.dict()['download'])
    upload = convert_bps_to_mbps(results.dict()['upload'])

    print("Internet speed: " + str("{:.1f}".format(download)) + "down/" +
          str("{:.1f}".format(upload)) + "up")

    # save results locally here for future plotting
    write_results_to_csv(results.csv(), header=results.csv_header(),
                         filename=args.output_file)

    if args.enable_tweet:
        t = get_twitter_account_info()
        # TODO: make this a user definable variable
        # if less than 10Mbps
        if (download < args.threshold):
            tweet = ("My internet speed is " +
                     str("{:.1f}".format(download)) + "down/" +
                     str("{:.1f}".format(upload)) +
                     "up but I pay for 150down/5up in the Bay Area! Why" +
                     " is that? #comcast #xfinity #comcastsucks")
            t.update_status(status=tweet)
            print("Internet too slow tweet sent: " + tweet)
        else:
            print("No tweet sent.")
    else:
        print("No tweet sent")

    print("Speed test complete")


if __name__ == '__main__':
    main()
