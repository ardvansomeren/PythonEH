#! /usr/bin/env python

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP range to scan for MAC addresses 10.0.2.1/24")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an ip range, use --help for more info.")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip" : element[1].psrc , "mac" : element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("\n\nIP\t\tMAC Address\n---------------------------------")
    for client in results_list:
        print(client["ip"] + "\t" + client["mac"])
    print("\n")


options = get_arguments()
print("\nScanning IP (range) : " + options.target)

# scan_result = scan("10.0.2.1/24")
scan_result = scan(options.target)
print_result(scan_result)