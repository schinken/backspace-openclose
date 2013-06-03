import sys
import re
import commands
import threading

from collections import defaultdict

class NmapCollector(threading.Thread):

    hosts = {}

    def __init__(self, network):
        threading.Thread.__init__(self)
        self.network = network

    def run(self):

        cmd = 'nmap -sP -n %s' % (self.network,)
    
        (status, output) = commands.getstatusoutput(cmd)

        if status:
            sys.stderr.write('Error running nmap command')
            return False

        self.hosts = self.parse(output)

    def parse(self, output):

        hosts = defaultdict()

        # parse all mac and ip combinations from string
        matches = re.findall(r'scan report for\s+((?:\d{1,3}\.){3}\d{1,3}).*?MAC Address:\s+((?:[0-9A-F]{2}\:){5}[0-9A-F]{2})', output, re.M | re.S)
        for match in matches:
            ip = match[0]
            hosts[ip] = match[1].lower()

        return hosts

    def get_hosts(self):
        return self.hosts

if __name__ == '__main__':

    tst = NmapCollector('10.1.20.100-250')
    tst.start()

    tst.join()
