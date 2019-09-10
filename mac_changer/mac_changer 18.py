#! /usr/bin/env python

# start pycharm manualy | cd /opt/pycharm-community-2019.1.3/bin | ./pycharm.sh

import subprocess
import optparse

# create a parser object
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address for the interface")

(options, arguments) = parser.parse_args()

interface = options.interface
new_mac = options.new_mac

# ifconfig eht0 down
# ifconfig eth0 hw ether 00:11:22:33:44:55
# ifconfig eth0 up

# interface = "eth0"
# new_mac = "00:11:22:33:44:55"
# org_mac = "08:00:27:89:03:db"
#
# # Python3 - input() | Python2 - raw_input()
# interface = input("What interface are you going to change > ")
# new_mac = input("What is the new MAC address for the interface: " + interface + " > ")


print("[+] Changing MAC address for: " + interface + ", to " + new_mac)


# --- original code ---
# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)
#
# The original code is not very secure. It can be hyjacked. when starting executing the code it will ask for user input:
# What interface are you going to change >
# The first input can be simply eth0, for the interface. By separating the input with a ; you can inject a second
# command that will run after the first command is executed. For instance ls will show the directory
# from where the code was run.


# subprocess.call("ifconfig " + interface + " down", shell=True)
# # subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])

