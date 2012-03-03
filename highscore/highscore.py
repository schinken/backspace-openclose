#!/usr/bin/python

import commands
import re

import MySQLdb
import MySQLdb.cursors

import datetime
import time

import yaml

timeout = datetime.timedelta(minutes=20)

configFile = 'config.yaml'

def calculateTime( nickname, dbcron ):

    macaddrs = []
    dbcursor = dbcron.cursor()


    dbcursor.execute('SELECT macaddr FROM mac_to_nick WHERE nickname = %s and privacy < 3', nickname );
    for record in dbcursor:
        macaddrs.append( record['macaddr'] )

    if not macaddrs:
        return 0


    query = 'SELECT erfda FROM alive_hosts WHERE macaddr IN( %s ) GROUP by erfda ORDER by erfda ASC'

    inStr = ', '.join( list( map( lambda x: '%s', macaddrs ) ) )
    query = query % inStr

    lastDt = None
    beginDt = None

    timePresent = datetime.timedelta()
    
    dbcursor.execute( query, macaddrs )
    for record in dbcursor:

        currentDt = record['erfda']

        if lastDt and lastDt + timeout < currentDt:
            timePresent += (lastDt - beginDt)

            # current block closed, next block starts at curTs
            beginDt = None


        # if beginTs is not set, set it to the current timestamp
        # so we have the begin of the "present"-block saved
        if not beginDt:
            beginDt = currentDt

        # schleppzeiger
        lastDt = currentDt


    if lastDt:
        endDt = datetime.datetime.now()

        if lastDt + timeout < endDt:
            timePresent += ( lastDt - beginDt )

    print nickname, "was", timePresent, "present"

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
    dbcron = MySQLdb.connect ( host=cfg['mysql_host'], user=cfg['mysql_user'], passwd=cfg['mysql_pass'], db=cfg['mysql_name'], cursorclass=MySQLdb.cursors.SSDictCursor )
    dbcron2 = MySQLdb.connect ( host=cfg['mysql_host'], user=cfg['mysql_user'], passwd=cfg['mysql_pass'], db=cfg['mysql_name'], cursorclass=MySQLdb.cursors.SSDictCursor )

    dbcursor = dbcron.cursor()

    dbcursor.execute('SELECT nickname FROM mac_to_nick GROUP by nickname')
    for entry in dbcursor:
        calculateTime( entry['nickname'], dbcron2 );

    dbcursor.close()
    dbcron.close()

if __name__ == "__main__":
    main()
