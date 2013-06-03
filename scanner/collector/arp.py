import sys
import re
import commands
import threading

from iptools.ipv4 import ip2long
from collections import defaultdict

class ArpCollector(threading.Thread):

    hosts = {}

    def __init__(self, network):
        threading.Thread.__init__(self)

        # process network range
        m = re.search(r'((?:\d{1,3}\.){3})(\d{1,3})-(\d{1,3})', network)
        if not m:
            sys.stderr.write('Invalid ip adress format "%s"' % (network,))
            return False

        net = m.group(1)

        self.ip_begin = net + m.group(2)
        self.ip_end = net + m.group(3)

    def run(self):

        cmd = '/usr/bin/fping -a -q -g %s %s 2> /dev/null' % (self.ip_begin,
                self.ip_end) 

        # we dont use the status code here, because fping returns strange
        # values.
        (status, output) = commands.getstatusoutput(cmd)

        (status, output) = commands.getstatusoutput('arp -a')

        if status:
            sys.stderr.write('Error running command "arp -a"')
            return False

        self.hosts = self.parse(output)

    def parse(self, output):

        hosts = defaultdict()

        ipl_begin = ip2long(self.ip_begin)
        ipl_end = ip2long(self.ip_end)

        # parse all mac and ip combinations from string
        matches = re.findall(r'\(((?:\d{1,3}\.){3}\d{1,3})\) at ((?:[0-9A-F]{2}\:){5}[0-9A-F]{2})', output, re.I)
        for match in matches:
            ip = match[0]
            ipl_cur = ip2long(ip)
            if ipl_cur >= ipl_begin and ipl_cur <= ipl_end:
                hosts[ip] = match[1].lower()

        return hosts

    def get_hosts(self):
        return self.hosts

if __name__ == '__main__':

    tst = ArpCollector('10.1.20.100-250')
    tst.start()

    tst.join()
