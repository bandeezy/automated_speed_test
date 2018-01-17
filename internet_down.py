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
import time

from argparse import ArgumentParser

try:
    import tweepy
except ImportError:
    print("Could not import module 'tweepy'. Has it been installed?")
    sys.exit(1)


def parse_args():
    desc = 'Checks internet status and informs Comcast via Twitter that'\
            'internet is down.\n'
    parser = ArgumentParser(description=desc)
    parser.add_argument('--enable_tweet', action='store_true', default=False)

    args = parser.parse_args()

    return args


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


# TODO: add as library
def connected_to_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout);
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False


def main():
    args = parse_args()

    while True:
        if not connected_to_internet():
            start_time = datetime.datetime.now()
            while not connected_to_internet():
                pass  # do nothing
            end_time = datetime.datetime.now()
            time_diff = end_time - start_time

            ping = 0
            download = 0
            upload = 0
            test_complete = 0
            # TODO: configure UTC time to either have T
            #       or remove T from the speedtest UTC time
            results_csv = "NA,NA,NA," + str(datetime.datetime.utcnow()) + ",NA," + str(ping) + "," + str(download) + "," + str(upload) + "," + str(time_diff.seconds) 
            write_results_to_csv(results_csv)

            if args.enable_tweet:
                t = get_twitter_account_info()
                tweet = "@comcast @comcastcares @xfinity why has my internet been down for {} seconds in Mountain View, CA? #comcastoutage #xfinityoutage".format(time_diff.seconds)
                t.update_status(status=tweet)
                print("Internet down tweet sent: " + tweet)
            else:
                print("Internet was down for {} seconds but tweet was not sent since argument was not set.".format(time_diff.seconds))
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    main()
