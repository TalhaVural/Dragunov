import sys
import time
from termcolor import colored
import dns.resolver
import dns.query
import dns.zone
import random
import socket
import os
import re

usage = '''
    Dragunov SVD
                 _    _    _
                |_)=D=N=S=(_|
 A____________ _____H___H___o    _____
O____________<^       ====__~`\_/    /`~~|
              `\_________(_)>.  ___--'   |
                              \/   `-----'
    DnsHunter
------------------------------------------------
	https://github.com/emrekybs
		
'''
us = 'Usage: python3 dragunov.py "domain" / Example: "python3 dragunov.py google.com"\n'
if len(sys.argv) < 2:
	print(colored(usage, 'blue', attrs=['bold']))
	print(us)
	sys.exit()

print(colored(usage, 'blue', attrs=['bold']))
print(colored("[+] Initiating Zone Transfer", 'green', attrs=['bold']))
print(colored("=================================================================================================", 'red', attrs=['bold']))
time.sleep(2)

domain = sys.argv[1]

ns_server_list = []
def ns_server(domain):
	for rdata in dns.resolver.resolve(domain, 'NS'):
		ns = []
		count1 = 0
		while count1 < (len(rdata.target) - 1):
			ns.append(random.randint(0,9))
			count1 += 1
		count = 0
		while count < (len(rdata.target) - 1):
			p = str((rdata.target[count]).decode('utf-8'))
			ns[count] = p
			#ns_server_list.append(ns)
			count += 1
		i = 0
		domn = ""
		while i < len(ns):
			domn += ("." + ns[i])
			i += 1
		domn = domn.replace('.', '', 1)
		ns_server_list.append(domn) 
		ns = []

ns_server(domain)

print(colored("\n[+] Found Name Servers", 'green', attrs=['bold']))
print(ns_server_list)
print(colored("\n-----------------------------------------------------------------------------------", 'blue', attrs=['bold']))

def zone_tsfr(domain, name_server_ip):
	os.system(f'host -l {domain} {name_server_ip}')

for ns_name in ns_server_list:
	store = os.popen(f"host {ns_name}").read().strip()
	ns_name_ip_list = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", store)
	final_ip = ns_name_ip_list[0]
	print(colored(f"[+] Attempting Zone Transfer Against {ns_name}", 'green', attrs=['bold']))
	zone_tsfr(domain, final_ip)
	print(colored("\n========================================================================", 'blue', attrs=['bold']))
