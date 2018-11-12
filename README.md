# README
## Intention
The intention of both the internet_speed.py and internet_down.py scripts is
for them to be run as a cronjob, regularly checking the internet speed and
connectivity, respectively.

WARNING: enabling the twitter API can result in suspension of your Titter
account as "spamming" a user that has not made contact with you (such as
Comcast) violates Twitter's user agreement. Proceed with caution.

## Installing dependencies
### Speedtest
Install speedtest for your python distro: https://pypi.org/project/speedtest-cli/

### Tweepy - twitter API for python
TODO: add instructions

## Other necessities for setup
### Creating file for twitter credentials
TODO: add file structure and example

## Running script
### cronjob
This script was initially intended to run as a cronjob, such that internet
speed trends can be plotted over time. Once a decent history is collected,
thresholds can be set for which Comcast will be notified via twitter.


# General things to do
* Use logger library instead of print, include debugs
* Add option of passing twitter credentials directly to script
* Check compatibility of all scripts with python2 and 3
