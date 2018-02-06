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


def write_results_to_csv(data):
    print("Writing results to CSV")
    header = "server_id,sponsor,server_name,timestamp (utc),distance (mi),ping (ms),download (Mbps),upload (Mbps), downtime (s)"
    filename = "/home/nick/stored_data/internet_speed_test/data.csv"

    # if file doesn't exist, creat it with the corresponding header
    if not (os.path.isfile(filename)):
        out_file = open(filename, 'w')
        out_file.write(header + "\n")
    else:
        out_file = open(filename, 'a')

    out_file.write(data + "\n")
    out_file.close()

