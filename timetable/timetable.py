#!/usr/bin/python


import MySQLdb
import MySQLdb.cursors

import datetime
import yaml


class TimeTable:

    timeout = datetime.timedelta(minutes=20)

    def __init__( self, nickname, database ):
        self.nickname = nickname
        self.database = database

    def getMACs(self):

        dbCur = self.database.cursor()
        dbCur.execute('SELECT macaddr FROM mac_to_nick WHERE nickname = %s and privacy < 3', nickname );

        MACs = []
        for record in dbCur:
            MACs.append( record['macaddr'] )

        dbCur.close()

        return MACs

    def getTimeTable(self, mac=None):

        if mac:
            MACs = [ mac ]
        else:
            MACs = self.getMACs()

        if not MACs:
            return []

        timetable = []

        dbCur = self.database.cursor()
        query = self.buildQueryByMACs( MACs )

        lastDt  = None
        beginDt = None

        dbCur.execute( query, MACs )
        for record in dbCur:
            currentDt = record['erfda']

            if lastDt and lastDt + self.timeout < currentDt:
                timetable.append( (beginDt, lastDt ) )

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

            if lastDt + self.timeout < endDt:
                timetable.append( (beginDt, lastDt ) )

        dbCur.close()

        return timetable


    def getTimePresent(self, timetable=None, macaddr=None):

        if not timetable:
            timetable = self.getTimePresent(mac=macaddr)

        present = datetime.timedelta()
        for record in timetable:
            present += ( record[1] - record[0] )


        return present

    def buildQueryByMACs(self, MACs ):

        query = 'SELECT erfda FROM alive_hosts WHERE macaddr IN( %s ) GROUP by erfda ORDER by erfda ASC'
        inStr = ', '.join( list( map( lambda x: '%s', MACs ) ) )

        return query % inStr

