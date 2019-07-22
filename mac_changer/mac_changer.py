#! /usr/bin/env python

# start pycharm manualy | cd /opt/pycharm-community-2019.1.3/bin | ./pycharm.sh

# original mac address: 08:00:27:89:03:db

"""
ifconfig eht0 down
ifconfig eth0 hw ether 00:11:22:33:44:55
ifconfig eth0 up
"""

import subprocess

#subprocess.call("ifconfig", shell=True)


subprocess.call("ifconfig eth0 down", shell=True)
subprocess.call("ifconfig eth0 he ether 00:11:22:33:44:55", shell=True)
subprocess.call("ifconfig eth0 up", shell=True)