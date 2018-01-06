#!/usr/bin/env python

import os
import sys
import csv
import datetime

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
#try:
#    from hurry.filesize import size
#except ImportError:
#    print("Could not import module 'hurry.filesize'. Has it been installed?")
#    sys.exit(1)


def parse_arguments():
    desc = 'Checks internet speed and informs Comcast via Twitter that internet is slow or down.\n'\
           'Additionally, this records internet speed data for future plotting.\n'

    parser = ArgumentParser(description=desc)
    parser.add_argument('--enable_tweet', action='store_true', default=False)
    
    args = parser.parse_args()

    return args

def get_speedtest_data():
    print("Testing internet speed")
    servers = []

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()

    results_dict = s.results.dict()

    return results_dict


def write_results_to_csv(date_and_time, ping, download, upload):
    print("Writing results to CSV")

    out_file = open('/var/speedtest/data.csv', 'a')
    writer = csv.writer(out_file)
    # TODO: properly separate date and time
    writer.writerow((date_and_time, ping, download, upload))
    out_file.close()


def get_twitter_account_info():
    print("Retrieving twitter account info")
    
    auth_file = open('/var/speedtest/twitter.txt', 'r')
    alist = []
    for line in auth_file:
        alist.append(line.strip())
    auth_data = auth_file.readlines()

    cfg = {
      "consumer_key"        : alist[2],
      "consumer_secret"     : alist[3],
      "access_token"        : alist[0],
      "access_token_secret" : alist[1]
      }
      
    auth_file.close()
    t = get_api(cfg)
    return t


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    internet_conn = False

    args = parse_arguments()


    try:
        # TODO: necessary if speedtest just fails when no internet is connected?
        os.popen("ip route get 8.8.8.8")
        
        # run speedtest
        results = get_speedtest_data()

        ping = results['ping']
        download = (results['download']/1024)/1024
        upload = (results['upload']/1024)/1024
        test_complete = 1
    except:
        ping = 0
        download = 0
        upload = 0
        test_complete = 0
    
    # save results locally here for future plotting
    write_results_to_csv(datetime.datetime.now(), ping, download, upload)

    t = get_twitter_account_info()

    if test_complete and args.enable_tweet:
        try:
            tweet = ("my internet speed is" + str("{:.1f}".format(download)) + "down/" + str("{:.1f}".format(upload)) + "but I pay for 100down/10up in the Bay Area! Why is that?")
            #tweet = ("@comcast @comcastcares @xfinity my internet speed is" + str("{:.1f}".format(download)) + "down/" + str("{:.1f}".format(upload)) + "but I pay for 100down/10up in the Bay Area! Why is that? #comcast")
            t.update_status(status=tweet)
        except:
            # TODO: have the program wait until internet is restored, and output internet downtime
            tweet = "why has my internet been down for X?"
            #tweet = "@comcast @comcastcares @xfinity why has my internet been down for X? #comcastoutage #xfinityoutage"
            t.update_status(status=tweet)
            print("No internet connection, therefore no tweet can be generated.")
    else:
        print("Internet speed: " + str("{:.1f}".format(download)) + "down/" + str("{:.1f}".format(upload)) + "up\nNo tweet sent.")


if __name__ == '__main__':
    main()
    print("Speed test complete")
