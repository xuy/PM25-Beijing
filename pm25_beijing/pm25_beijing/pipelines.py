from datetime import datetime,timedelta
from os import path as p
import sqlite3 as sqlite

# Things that are stored into the sqlite database.
# 1. UTC stamp for the PM25 data.
# 2. Saturation value of the data.
# 3. UTC timestamp of the fetched date.
""" Convert a time value like 22:00 to UTC time.
    Beijing is UTC+8. My local time is UTC-5."""
class DateUtil(object):
    def __init__(self):
        self.reference_point = datetime.utcnow() + \
        timedelta(hours=8) + timedelta(hours=-24)
    """ Infer the correct time for the value."""
    def infer(self, time):
        if time == u'0:00':
            self.reference_point += timedelta(hours=24)
        return str(self.reference_point.date()) + " " + str(time)

class ProcessPipeline(object):
    def __init__(self):
        self.date_util = DateUtil()
    def process_item(self, item, spider):
        item['hour'] = self.date_util.infer(item['hour'])
        item['saturation'] = float(item['saturation'])
        return item

class StorePipeline(object):
    def __init__(self):
        self.database = p.abspath(p.join(p.split(__file__)[0], 'pm25.db'))
        if not p.exists(self.database):
            # create a dummy database file.
            f = open(self.database, "w")
            f.close()
            # Initlize the table to an initial layout.
            
            self.connection = sqlite.connect(self.database)
            self.cur = self.connection.cursor()
            self.cur.execute("""CREATE TABLE pm25(Hour TEXT, Saturation REAL, Timestamp  TEXT)""")
            self.connection.commit()
            self.cur.close()
        self.connection = sqlite.connect(self.database)
        self.cur = self.connection.cursor()
    
    def __del__(self):
        self.connection.commit()
        self.connection.close()    
        
    def process_item(self, item, spider):
        self.cur.execute('insert into pm25 values(?,?,?)',\
            [item['hour'], item['saturation'], item['timestamp']])
        self.connection.commit()    
        return item