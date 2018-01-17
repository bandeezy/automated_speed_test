#!/usr/bin/env python

'''
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

import os
import sys
import datetime
import socket

from argparse import ArgumentParser

try:
    import speedtest
except ImportError:
    print("Could not import module 'speedtest'. Has it been installed?")
    sys.exit(1)
try:
    import tweepy
except ImportError:
    print("Could not import module 'tweepy'. Has it been installed?")
    sys.exit(1)


def parse_args():
    desc = 'Checks internet speed and informs Comcast via Twitter that'\
            'internet is slow or down.\nAdditionally, this records internet'\
            'speed data for future plotting.\n'

    parser = ArgumentParser(description=desc)
    parser.add_argument('--enable_tweet', action='store_true', default=False)

    args = parser.parse_args()

    return args


def get_speedtest_data():
    print("Testing internet speed")
    servers = []

    s = speedtest.Speedtest()
    s.get_servers(servers)
    # select server with lowest latency
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=False)

    return s.results.dict(), s.results.csv()


# TODO: add as library
def write_results_to_csv(data):
    print("Writing results to CSV")
    header = "server_id,sponsor,server_name,timestamp (utc),distance (mi),ping (ms),download (Mbps),upload (Mbps),downtime (s)"
    filename = "/home/nick/stored_data/internet_speed_test/data.csv"

    # if file doesn't exist, creat it with the corresponding header
    if not (os.path.isfile(filename)):
        out_file = open(filename, 'w')
        out_file.write(header + "\n")
    else:
        out_file = open(filename, 'a')

    out_file.write(data + "\n")
    out_file.close()


# TODO: add as library
def get_twitter_account_info():
    print("Retrieving twitter account info")
    auth_file = open('/home/nick/stored_data/internet_speed_test/twitter.txt', 'r')
    alist = []
    for line in auth_file:
        alist.append(line.strip())
    # auth_data = auth_file.readlines()

    cfg = {
        "consumer_key"        : alist[2],
        "consumer_secret"     : alist[3],
        "access_token"        : alist[0],
        "access_token_secret" : alist[1]
    }

    auth_file.close()
    t = get_twitter_api(cfg)
    return t


# TODO: add as library
def get_twitter_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    args = parse_args()

    try:
        # run speedtest
        results, results_csv = get_speedtest_data()

        ping = results['ping']
        download = (results['download']/1024)/1024
        upload = (results['upload']/1024)/1024
        test_complete = 1
    # TODO: add exception type here
    except:
        return False

    # save results locally here for future plotting
    write_results_to_csv(results_csv)

    if args.enable_tweet:
        try:
            t = get_twitter_account_info()
            # if less than 10Mbps
            if (download < 10.0):
                tweet = ("@comcast @comcastcares @xfinity my internet speed is " + str("{:.1f}".format(download)) + "down/" + str("{:.1f}".format(upload)) + "up but I pay for 150down/5up in the Bay Area! Why is that? #comcast")
                t.update_status(status=tweet)
                print("Internet too slow tweet sent: " + tweet)
            else:
                print("No tweet sent.")
        except:  # TODO: add exception type here
            return False
    else:
        print("No tweet sent")
    
    print("Internet speed: " + str("{:.1f}".format(download)) + "down/" + str("{:.1f}".format(upload)) + "up")
    return True


if __name__ == '__main__':
    main()
    print("Speed test complete")
