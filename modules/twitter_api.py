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

try:
    import tweepy
except ImportError:
    print("Could not import module 'tweepy'. Has it been installed?")
    sys.exit(1)


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


def get_twitter_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

