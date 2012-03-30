
import yaml
import MySQLdb
import MySQLdb.cursors
from timetable import TimeTable

import datetime
import operator

configFile = 'config.yaml'

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

    collector = {}
    dbcursor.execute("SELECT DISTINCT nickname FROM mac_to_nick")
    for entry in dbcursor:

        nickname = str.lower( entry['nickname'] )
        objTimetable = TimeTable( nickname,  dbcron2 )
        collector[ nickname ] = objTimetable.getTimeTable()

    dbcursor.close()
    dbcron.close()

    for nick, table in collector.iteritems():
        getRelation( nick, collector )


def getRelation( nick, collection ):

    master = collection[ nick ]

    relation = {}

    print "#"*60
    print "Calculation relation for", nick
    print "#"*60

    for victim, table in collection.iteritems():

        # ignore own nickname - doesnt make sense to calculate the correlation to yourself
        if victim == nick:
            continue

        relation[ victim ] = datetime.timedelta()

        for times_victim in table:

            victim_begin = times_victim[0]
            victim_end   = times_victim[1]

            for times_master in master:

                master_begin = times_master[0]
                master_end   = times_master[1]

                begin = max( victim_begin, master_begin )
                end   = min( victim_end,   master_end   )

                if begin < end:
                    relation[ victim ] += ( end-begin )

    relation = sorted( relation.iteritems(), reverse=True , key=operator.itemgetter(1) )

    for (key, value) in relation:
        print key, "=>", value


if __name__ == "__main__":
    main()