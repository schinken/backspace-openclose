#!/usr/bin/python

from collector import ubiquiti, arp, nmap
from iptools.ipv4 import ip2long

import MySQLdb
import MySQLdb.cursors

import iptools
import settings

def main():

    collectors = []

    # ====== add ubuquiti ======
    ubnt = settings.ubiquiti

    x = ubiquiti.Collector(settings.network, ubnt['host'], ubnt['user'], ubnt['pass'])
    x.start()

    collectors.append(x)

    # ====== add arp =======
    x = arp.Collector(settings.network)
    x.start()

    collectors.append(x)

    # ====== add nmap ======
    x = nmap.Collector(settings.network)
    x.start()

    collectors.append(x)


    # waiting for collectors...
    for collector in collectors:
        collector.join()

    # results
    print "The results are in!"

    hosts = {}
    for collector in collectors:
        print collector.get_hosts()
        hosts = dict(hosts.items() + collector.get_hosts().items())

    # create database connection
    dbcron = MySQLdb.connect(host=settings.mysql_host,
                             user=settings.mysql_user,
                             passwd=settings.mysql_pass,
                             db=settings.mysql_name)

    # write hosts to database
    dbcursor = dbcron.cursor()

    # add ALL THE HOSTS to the database
    for ip,mac in hosts.iteritems():
        longip = ip2long(ip) 
        dbcursor.execute("INSERT INTO alive_hosts (macaddr, iplong, erfda) VALUES ('%s', %d, NOW())" % (mac.lower() , longip))

    dbcursor.close()

    # close database connection
    dbcron.commit()
    dbcron.close()

if __name__ == "__main__":
    main()
