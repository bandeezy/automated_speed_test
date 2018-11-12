#!/usr/bin/env python

__doc__ = '''
This module provides a function to write csv results to a file from the
speedtest
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

import os


def write_results_to_csv(data,
                         header,
                         filename="/tmp/internet_speed_test/data.csv"):
    print("Writing results to CSV stored here: {}".format(filename))

    # if file doesn't exist, create it with the corresponding header
    if not (os.path.isfile(filename)):
        with open(filename, 'w') as out_file:
            out_file.write(header + "\n")

    with open(filename, 'a') as out_file:
        out_file.write(data + "\n")
