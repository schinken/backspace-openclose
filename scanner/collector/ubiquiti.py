import threading
import re
import sys

from unifi.controller import Controller
from iptools.ipv4 import ip2long
from collections import defaultdict

class Collector(threading.Thread):

    hosts = {}

    def __init__(self, network, controller, username, password):
        threading.Thread.__init__(self)

        self.username = username
        self.password = password
        self.controller = controller

        # process network range
        m = re.search(r'((?:\d{1,3}\.){3})(\d{1,3})-(\d{1,3})', network)
        if not m:
            sys.stderr.write('Invalid ip adress format "%s"' % (network,))
            return False

        net = m.group(1)

        self.ip_begin = net + m.group(2)
        self.ip_end = net + m.group(3)

    def run(self):

        hosts = defaultdict()

        ipl_begin = ip2long(self.ip_begin)
        ipl_end = ip2long(self.ip_end)

        try:
            c = Controller(self.controller, self.username, self.password)

            for client in c.get_clients():

                ip = client.get('ip', False)
                if not ip:
                    continue

                ipl_cur = ip2long(ip)
                if ipl_cur >= ipl_begin and ipl_cur <= ipl_end:
                    hosts[ip] = client['mac'].lower()

            self.hosts = hosts

        except:
            # somethimes a weird SSL Handshake errors appears in combination
            # with the ubiquiti tomcat server.
            #
            # see: http://stackoverflow.com/questions/14167508/intermittent-sslv3-alert-handshake-failure-under-python
            return False

    def get_hosts(self):
        return self.hosts

if __name__ == '__main__':

    tst = Collector('10.1.20.100-250', '10.1.20.5', 'root', 'xxxx')
    tst.start()

    tst.join()

    print tst.get_hosts()
