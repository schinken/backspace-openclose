#!/usr/bin/python

import commands
import re

import MySQLdb
import MySQLdb.cursors

import iptools
import settings
import sys


def run_nmap(network):

    cmd = 'nmap -sP -n ' + network
   
    (status, output) = commands.getstatusoutput(cmd)

    if status:
        sys.stderr.write('Error running nmap command')
        return None

    return output


def get_hosts(network):

    output = run_nmap(network)
    hosts = []

    # parse all mac and ip combinations from string
    matches = re.findall(r'scan report for\s+((?:\d{1,3}\.){3}\d{1,3}).*?MAC Address:\s+((?:[0-9A-F]{2}\:){5}[0-9A-F]{2})', output, re.M | re.S)
    for match in matches:
        hosts.append({'ip': match[0], 'mac': match[1]})

    return hosts

def write_hosts(hosts, db):

    dbcursor = db.cursor()

    # add ALL THE HOSTS to the database
    for host in hosts:
        longip = iptools.ip2long(host['ip']) 
        dbcursor.execute("INSERT INTO alive_hosts (macaddr, iplong, erfda) VALUES ('%s', %d, NOW())" % (host['mac'].lower() , longip))

    dbcursor.close()

def main():

    # create database connection
    dbcron = MySQLdb.connect(host=settings.mysql_host,
                             user=settings.mysql_user,
                             passwd=settings.mysql_pass,
                             db=settings.mysql_name)

    # parse host string, returned from nmap
    hosts  = get_hosts(settings.network)

    # write hosts to database
    write_hosts(hosts, dbcron)

    # close database connection
    dbcron.commit()
    dbcron.close()

if __name__ == "__main__":
    main()
