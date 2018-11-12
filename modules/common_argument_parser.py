#!/usr/bin/env python

__doc__ = '''
This is a common argument parser
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

from argparse import ArgumentParser
import os


def parse_and_validate_arguments(script_filename, script_docstring,
                                 threshold=False):
    output_file_default = '/tmp/internet_speed_test/data.csv'
    credential_file_default = os.path.join(
        os.path.dirname(os.path.realpath(script_filename)),
        "twitter_auth_file.json")

    parser = ArgumentParser(description=script_docstring)
    parser.add_argument('-o', '--output-file',
                        default=output_file_default,
                        help='Output filename and location for CSV '
                             '(default: {})'.format(output_file_default))
    parser.add_argument('--enable-tweet', action='store_true', default=False,
                        help='If argument is set, a tweet is sent.')
    parser.add_argument('-c', '--credential-file',
                        default=credential_file_default,
                        help='Credential file used to interact with the '
                             'Twitter API '
                             '(default: {})'.format(credential_file_default))
    if threshold:
        threshold_default = 10.0
        parser.add_argument('-t', '--threshold', default=threshold_default,
                            help='Download speed threshold at which a tweet '
                                 'is sent. This is only valid for checking '
                                 'internet speed, not connectivity '
                                 '(default: {})'.format(threshold_default))

    args = parser.parse_args()

    directory = os.path.dirname(args.output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    return args
