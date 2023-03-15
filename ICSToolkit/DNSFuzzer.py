#Author: Logan Gleason  
#DNS Fuzzer

import socket
import dns.resolver as dnsr

target = input("Target server: ")
path_to_wordlist = input("File path to wordlist: ")
query_type = input("Enter query type: ")

with open(path_to_wordlist, 'r') as f:
    wordlist = f.readlines()

for word in wordlist:
    query = word.strip()
    try:
        resolver = dnsr.Resolver()
        resolver.nameservers = target
        response = resolver.query(query,query_type)
        resolver.timeout()
        for data in response:
            print(query, data)
    except Exception as e:
        print(query, e)
