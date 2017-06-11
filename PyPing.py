# -*- coding: utf-8 -*-

"""
Copyright 2016
Alexander Kozhinov <alexanderkozhinov@yandex.com>
"""

import subprocess
import click
import time
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 PyPing.py <start ipv4> <end ipv4>")
        sys.exit()
    start_ip = sys.argv[1]
    end_ip = sys.argv[2]

    # Provide delimiter and number of numeric groups control:
    delim = "."
    start_ip = start_ip.split(delim)
    end_ip = end_ip.split(delim)
    if len(start_ip) != 4 or len(end_ip) != 4:
        print("Error: One of IP's is wrong. Should be: xxx.xxx.xxx.xxx")
        sys.exit()

    # Convert lists of strings to numbers and control
    # each value to be <= 255 and >= 0
    start_ip = [int(x) for x in start_ip]
    end_ip = [int(x) for x in end_ip]

    for x in start_ip:
        if x > 255 or x < 0:
           print("Error: One of IP's is wrong: Each number"
                 " should be between 0 and 255!")
           sys.exit()
    
    for x in end_ip:
        if x > 255 or x < 0:
           print("Error: One of IP's is wrong: Each number"
                 " should be between 0 and 255!")
           sys.exit()

    # Control both ip's are from same ip range:
    for i in range(len(start_ip)- 1):
        if start_ip[i] != end_ip[i]:
           print("Error: IP's range must be the same!")
           sys.exit()

    # Start and end definition:
    s = start_ip[-1] if start_ip[-1] < end_ip[-1] else end_ip[-1]
    e = start_ip[-1] if start_ip[-1] > end_ip[-1] else end_ip[-1]
    
    # Provide ping:
    d = "."
    start_ip = start_ip[:len(start_ip)-1]
    str_ip = ''.join([(str(x) + d) for x in start_ip])

    active_ips = list()
    print("Process ping:")
    start_time = time.time()
    with open(os.devnull, "wb") as limbo:
        with click.progressbar(range(s, e+1), fill_char='=', empty_char=' ') as bar:
            for i in bar:
                ip = str_ip + str(i)
                result = subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                                          stdout=limbo, stderr=limbo).wait()
                if not result:
                   active_ips.append(ip)
    end_time = time.time()
    print("Done in %s ms" % ((end_time - start_time) * 1000))
    print()

    # Print active ips:
    print("Active IPs:")
    for ip in active_ips:
        print(ip)
    print()  
    
    # Exit:
    sys.exit()
