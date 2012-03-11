__author__ = 'schinken'


from timetable import TimeTable

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

    dbcursor.execute('SELECT nickname FROM mac_to_nick GROUP by nickname')
    for entry in dbcursor:

        objTimetable = TimeTable( entry['nickname'], dbcron2 )

        print "Result for", entry['nickname'], ":", objTimetable.getTimePresent()

    dbcursor.close()
    dbcron.close()

if __name__ == "__main__":
    main()