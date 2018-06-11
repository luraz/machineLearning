#!/usr/bin/env python2

import sqlite3,os,time,pipes,psycopg2,pprint

try:
    import config as cfg
except ImportError:
    print "[ERROR] Please make a copy of 'congig_template.py' as 'ghostrCfgLocal.py' and customize it"

class Database:
    _instance = None
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.DB_NAME, cfg.DB_USER, cfg.DB_HOST, cfg.DB_PASSWORD))
        except Exception as e:
            print "[ERROR] cannot connect to database with error %s " % e
            self.connection = None

    def _createTables(self):
        for table in  DbObject.__subclasses__():
            # table.droptable()
            table.create(self)

    @classmethod
    def getInstance(cls):
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance 

    def reconnect(self):
        print "reconnecting to postgress....."
        self.connection.close()
        self.connection = None

        try:
            self.connection = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.DB_NAME, cfg.DB_USER, cfg.DB_HOST, cfg.DB_PASSWORD))
        except Exception as e:
            print "[ERROR] cannot connect to database with error %s " % e
            self.connection = None

class DbObject(object):
    FIELDS = []

    def __init__(self, db):
        self.db = db
        for f in self.FIELDS:
            setattr(self, f[0], None)

    @classmethod
    def create(cls, db):
        query = []
        for f in cls.FIELDS:
            query.append(" ".join(f))
        qm = ", ".join(query)
        query = "CREATE TABLE IF NOT EXISTS %s( %s )" % (cls.__name__,qm)
        print query
        try :
            c = db.connection.cursor()
            c.execute(query)
            db.connection.commit()
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query)
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                else:
                    print "connection is alive"
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query)
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                else:
                    print "connection is alive"
                    counter -= 1
        except Exception as e:
            print "[ERROR] unable to create table %s with error %s " % (cls.__name__,e)
            print query

            db.connection.rollback()
            return False
        c.close()
        print "created"
        return True

    @classmethod
    def addColumn(cls, name, typee):
        db = Database()
        query = "ALTER TABLE %s ADD %s %s" % (cls.__name__, name, typee)
        print query
        try:
            c = db.connection.cursor()
            c.execute(query)
            db.connection.commit()
        except Exception as e:
            print query
            print "[ERROR] unable to add column %s to table %s with error %s " % (name, cls.__name__, e)
            db.connection.rollback()
            return False
        c.close()
        return True

    @classmethod
    def removeColumn(cls, name):
        db = Database()
        query = "ALTER TABLE %s DROP COLUMN %s " % (cls.__name__, name)
        print query
        try:
            c = db.connection.cursor()
            c.execute(query)
            db.connection.commit()
        except Exception as e:
            print query
            print "[ERROR] unable to remove column %s from table %s with error %s " % (name, cls.__name__, e)
            db.connection.rollback()
            return False

        c.close()
        return True 

    @classmethod
    def droptable(cls):
        # db = Database.getInstance()
        db = Database()
        query = "DROP TABLE %s" % (cls.__name__,)
        
        try:
            c = db.connection.cursor()
            c.execute(query)
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query)
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                else:
                    print "connection is alive"
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query)
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                else:
                    print "connection is alive"
                    counter -= 1
        except Exception as e:
            print "[ERROR] unable to drop table %s with error %s" % (cls.__name__, e)
            print query
            db.connection.rollback()
            return False
        db.connection.commit()
        c.close()
        return True

    def delete(self, id):
        # db = Database.getInstance()
        db = Database()
        query = "DELETE FROM %s " % str((self.__class__.__name__))
        query += "WHERE id=%s"
        params =  (id,)
       
        try:
            c = db.connection.cursor()
            c.execute(query, params)
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                else:
                    print "connection is alive"
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                else:
                    print "connection is alive"
                    self.reconnect()
                    counter -= 1
        except Exception as e:
            print "[ERROR] unable to delete entry in table %s  with error %s " % (self.__class__.__name__, e)
            print query
            print params
            db.connection.rollback()
            return False
        db.connection.commit()
        c.close()
        return True

    #daca nu are setat id-ul se creaza un nou job cu valorile setate , altfel si updateaza jobul.
    def save(self):
        # db = Database.getInstance()
        db = Database()
        attrs = self.__dict__
        idd = None
        if self.id is None:
            #if the id is not set - insert into database
            fields = []
            values = []
            for field in attrs:
                if attrs[field] is not None and field != "db":
                    fields.append(str(field))
                    values.append(attrs[field])
            qm = "%s, " * (len(values) -1) + "%s"
            query = "INSERT INTO  %s ( %s ) values ( %s ) " % (self.__class__.__name__, ", ".join(fields), qm)
            params = tuple(values)
        else:
            #or else , update the database entry
            changes = []
            values = []
            for field in attrs:
                if attrs[field] is not None and field not in ["db", "id"]:
                    ch = " = ".join([str(field), "%s"])
                    changes.append(ch)
                    values.append(attrs[field])
            # values.append(self.id)
            query = "UPDATE %s SET %s  WHERE id=%s" %  (self.__class__.__name__, ", ".join(changes), self.id) 
            params = tuple(values)
        query += " RETURNING id"
        try:
            c = db.connection.cursor()
            c.execute(query, params)
            if self.id is None:
                idd = c.fetchone()[0]
            else :
                idd = self.id
            db.connection.commit()
        except psycopg2.OperationalError:
            print "error operational"
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        if self.id is None:
                            idd = c.fetchone()[0]
                            if idd is None or idd == "None":
                                continue
                        else:
                            idd = self.id
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in save operational error "
                    counter -= 1
        except psycopg2.DatabaseError:
            print repr(query)
            print repr(params)
            import traceback
            traceback.print_exc()
            # print "error operational"
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        if self.id is None:
                            idd = c.fetchone()[0]
                            if idd is None or idd == "None":
                                continue
                        else:
                            idd = self.id
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in save database error "
                    counter -= 1


        except Exception as e:   
            print "[ERROR] unable to save in table %s with error %s " % (self.__class__.__name__,e)
            print query
            print params
            if db.connection.closed > 0:
                db.reconnect()
            else:
                db.connection.rollback()
            return False
        if idd is None:
            return True
        c.close()
        return idd

    @classmethod
    def get(cls, id):
        # db = Database.getInstance()
        db = Database()
        query = "SELECT * FROM %s " % cls.__name__
        query += "WHERE id=%s"
       
        try :
            c = db.connection.cursor()
            c.execute(query, (id,))
            db.connection.commit()
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, (id,))
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in get operational error"
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, (id,))
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in get() database error "
                    counter -= 1
        except Exception as e :
            print "[ERROR] unable to get from table %s  with error %s" % (cls.__name__,e)
            print query
            return None
            db.connection.rollback()
        
        col_values = None
        col_names = None

        if c is not None and c.description is not None:
            col_names = [i[0] for i in c.description]
            col_values = c.fetchone()
        result = None
        if col_values is not None:
            result = {}
            for i in range(len(col_names)):
                result[col_names[i]] = col_values[i]
        c.close()
        return result

    # column_eq:value
    @classmethod
    def search(cls, **kwargs):
        # db = Database.getInstance()
        db = Database()
        params = []
        paramspag = []
        comparison = { "gt": ">", "gte" : ">=", "lt" : "<", "lte": "<=", "like" : "like", "eq" : "=" }
        if "pageSize" in kwargs and "pageNr" in kwargs:
            paramspag.append(kwargs["pageSize"])
            paramspag.append((int(kwargs["pageNr"])-1) * kwargs["pageSize"])
            del kwargs["pageSize"]
            del kwargs["pageNr"]
        elif "pageSize" in kwargs:
            del kwargs["pageSize"]
        elif "pageNr" in kwargs:
            del kwargs["pageNr"]
        
        query = "SELECT * FROM %s WHERE " % cls.__name__
        conditions = []
        
        try:
            for key in kwargs:
                tempconditions = []
                column, comp = key.rsplit("_",1)
                if type(kwargs[key]) == tuple:
                    for elem in kwargs[key]:
                        cond = " ".join([column, comparison[comp], "%s"])
                        params.append(elem)
                        if kwargs[key].index(elem) == len(kwargs[key])-1:
                            tempconditions.append(cond)
                        else:
                            tempconditions.append(cond + " or ")
                    if tempconditions != []:
                        conditions.append(" ".join(tempconditions))
                else:
                    cond = " ".join([column, comparison[comp], "%s"])
                    params.append(kwargs[key])
                    conditions.append(cond)
                

            query += " and ".join(conditions)
        except (ValueError, KeyError):
            print "[ERROR] params should be of the form : parameter_comparison=value (comparison: gt, gte, lt , lte , like , eq"
            return None
        if paramspag != []:
            query += " order by id DESC LIMIT %s OFFSET %s "
            params.append(paramspag[0])
            params.append(paramspag[1])

        
        try :
            c = db.connection.cursor()
            c.execute(query, params)
            col_names = [i[0] for i in c.description]
            db.connection.commit()
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        col_names = [i[0] for i in c.description]
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in search operational error "
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        col_names = [i[0] for i in c.description]
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                        continue
                else:
                    print "connection is alive in search database error "
                    counter -= 1
        except Exception as e :
            print "[ERROR] unable to search in table %s  with error %s" % (cls.__name__,e)
            print query
            print params
            if db.connection.closed > 0:
                db.reconnect()
            else:
                db.connection.rollback()
            return None

        try:
            col_values = c.fetchall()
        except Exception as e:
            print str(e)
            col_values = None
        results = None

        if col_values is not None and col_values != []:
            results = []
            for j in range(len(col_values)):
                result = {}
                for i in range(len(col_names)):
                    result[col_names[i]] = col_values[j][i]
                results.append(result)
        c.close()
        return results

    @classmethod
    def getAll(cls, sort="asc", pageSize=None, pageNr=None):
        db = Database()
        if pageSize is not None and pageNr is not None:
            query = "SELECT * from %s order by id DESC " % (cls.__name__)
            query +=  "LIMIT %s OFFSET %s"
            params = (pageSize, pageSize*(pageNr-1))
        else:
            query = "SELECT * from %s order by id %s " % (cls.__name__, sort)
            params = ()
        try :
            c = db.connection.cursor()
            c.execute(query, params)
            col_names = [i[0] for i in c.description]
            db.connection.commit()
        except psycopg2.OperationalError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        col_names = [i[0] for i in c.description]
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.OperationalError:
                        counter -= 1
                else:
                    print "connection is alive in getAll operational error"
                    counter -= 1
        except psycopg2.DatabaseError:
            counter = 5
            while counter > 0:
                if db.connection.closed != 0:
                    db.reconnect()
                    try:
                        c = db.connection.cursor()
                        c.execute(query, params)
                        col_names = [i[0] for i in c.description]
                        db.connection.commit()
                        counter -= 1
                        break
                    except psycopg2.DatabaseError:
                        counter -= 1
                else:
                    print "connection is alive in getAll database error "
                    counter -= 1
        except Exception as e :
            print "[ERROR] unable to getAll from table %s  with error %s " % (cls.__name__,e)
            print query
            print params
            if db.connection.closed > 0:
                db.reconnect()
            else:
                db.connection.rollback()
            return None

        try:    
            col_values = c.fetchall()
        except Exception as e :
            print str(e)
            return None
        results = None

        if col_values is not None and col_values != []:
            results = []
            for j in range(len(col_values)):
                result = {}
                for i in range(len(col_names)):
                    try:
                        result[col_names[i]] = col_values[j][i]
                    except Exception as e:
                        result[col_names[i]] = col_names[i]
                results.append(result)
        c.close()
        return results

class pcaps(DbObject):
    FIELDS = [
        ("id" , "SERIAL PRIMARY KEY "),
        ("name", "TEXT"),
        ("md5", "TEXT"),
        ("description", "TEXT"),
        ("incoming_timestamp", "TEXT"),
        ("sha256", "TEXT")
    ]


def main():
    pass
    # dbjs = Database()
    # p = pcaps(dbjs)
    # p.droptable()
    # dbjs._createTables()
  

if __name__ == "__main__":
    main()