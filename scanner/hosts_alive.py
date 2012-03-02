#!/usr/bin/python


import commands
import re

import MySQLdb
import MySQLdb.cursors

import iptools
import yaml

# starting connection to database

configFile = 'config.yaml'
network = '10.1.30.0/24'

def runNmap( network ):

    cmd = 'nmap -sP -n ' + network
   
    (status, output) = commands.getstatusoutput(cmd)

    if status:
        sys.stderr.write('Error running nmap command')
        return None

    return output


def getHosts( output ):

    hosts = []

    # parse all mac and ip combinations from string
    matches = re.findall(r'Host\s+((?:\d{1,3}\.){3}\d{1,3}).*?MAC Address:\s+((?:[0-9A-F]{2}\:){5}[0-9A-F]{2})', output, re.M | re.S )
    for match in matches:
        hosts.append({ 'ip': match[0], 'mac': match[1] })

    return hosts

def writeHosts( hosts, db ):


    dbcursor = db.cursor()

    # add ALL THE HOSTS to the database
    for host in hosts:
        longip = iptools.ip2long( host['ip'] ) 
        dbcursor.execute( "INSERT INTO alive_hosts (macaddr, iplong, erfda ) VALUES ( '%s', %d, NOW() )" % ( host['mac'].lower() , longip ) )

    dbcursor.close()

def main():

    # try to open yaml config file
    strConfig = open( configFile )
    if not strConfig:
        print "Error reading configfile", configFile
        exit(1)

    # try to parse yaml config string
    cfg = yaml.load( strConfig )
    if not cfg:
        print "Error parsing yaml config file"
        exit(1)

    # check if all required config keys are available
    for key in ['mysql_host', 'mysql_user', 'mysql_pass', 'mysql_name']:
        if key not in cfg:
            print "Missing parameter", key, "in configuration"
            exit(1)

    # create database connection
    dbcron = MySQLdb.connect ( host=cfg['mysql_host'], user=cfg['mysql_user'], passwd=cfg['mysql_pass'], db=cfg['mysql_name'] )

    # retrieve data from network
    result = runNmap( network )

    # parse host string, returned from nmap
    hosts  = getHosts( result )

    # write hosts to database
    writeHosts( hosts, dbcron )

    # close database connection
    dbcron.close()

if __name__ == "__main__":
    main()
