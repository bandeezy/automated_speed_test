# README
## Intention
The intention of the internet_speed.py script is to be run via cronjob at a
rate the user desires. This will regularly check internet speed, track the
data in a file and, if the option is set, notify comcast via twitter that
the internet speed has dropped below a threshold. The internet_down.py scripts
is intended to be run indefinitely in the background as it will track when and
for how long the internet connection has been disrupted.

WARNING: enabling the twitter API can result in suspension of your Titter
account IF you mentioned (@username) someone as "spamming" a user that has not
made contact with you (such as Comcast) violates Twitter's user agreement.
Proceed with caution.

## Installing dependencies
### Speedtest
Install speedtest for your python distro: https://pypi.org/project/speedtest-cli/

### Tweepy - twitter API for python
TODO: add instructions

## Other necessities for setup
### Populating file for twitter credentials
The twitter_auth_file.json serves as a template to be populated using
information obtained in the twitter developer account menu that can be seen
here: https://apps.twitter.com/

## Running script
### cronjob
This script was initially intended to run as a cronjob, such that internet
speed trends can be plotted over time. Once a decent history is collected,
thresholds can be set for which Comcast will be notified via twitter.


# General things to do
* Use logger library instead of print, include debugs
* Add option of passing twitter credentials directly to script
* Check compatibility of all scripts with python2 and 3
