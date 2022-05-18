#!/usr/bin/python3

import requests
import sys
import threading
from colorama import Fore, Style
import time


# TODO:
# Add in header injection or bearer token.
headers=''

def attacker(ip, paths):
    verbs = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']
    print(Fore.GREEN + 'Target: ' + ip + Style.RESET_ALL)
    for path in paths:
        if path.startswith("/"):
            target = '%s%s' % (ip, path)
        else:
            target = '%s/%s' % (ip, path)

        for verb in verbs:
            response = requests.request(verb, headers=headers, url=target, verify=False)
            
            # Print out codes we want. 
            if response.ok:
                colored = Fore.YELLOW + verb + " " + str(response.status_code) + " " + path + Style.RESET_ALL
                sys.stdout.write(colored)
                sys.stdout.flush()
            elif response.status_code == 400:
                colored = Fore.BLUE + verb + " " + str(response.status_code) + " " + path + Style.RESET_ALL
                sys.stdout.write(colored)
                sys.stdout.flush()
            elif response.status_code == 500:
                colored = Fore.RED + verb + " " + str(response.status_code) + " " + path + Style.RESET_ALL
                sys.stdout.write(colored)
                sys.stdout.flush()
       

def main():
    if len(sys.argv) != 3:
        print("(+) usage: %s <base_url> <wordlist>" % sys.argv[0])
        print("(+) eg: %s http://172.16.0.1:5000 api-endpoints.txt" % sys.argv[0])
        sys.exit(-1)

    ip = sys.argv[1]
    wordlist = open(sys.argv[2], 'r')
    paths = wordlist.readlines()

    # Start threading and peformance stat.
    try:
        start = time.perf_counter()
        t = threading.Thread(target=attacker, args=[ip, paths])
        t.start()
        print(f'Active Threads: {threading.active_count()}')
        t.join()
        finish = time.perf_counter()
        print(f'\nFinished in {finish-start} seconds') 
    except:
        print("BARF!")

if __name__ == "__main__":
    main()
