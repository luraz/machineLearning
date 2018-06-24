import os

try: 
    from pcapsDatabase import Database as dtb 
    from pcapsDatabase import pcaps, users
except ImportError as e:
    print ("[ERROR] unable to import from pcapsDatabase pcaps - if.py %s " % str(e))

import config as cfg

TABLE_HASH = {
    "users" : users, 
    "pcaps" : pcaps
}

class dbServicePcaps:
    def __init__(self, typee):
        db = dtb()
        self.dbObject = TABLE_HASH[typee](db)

    def uninitTable(self):
        for key in self.dbObject.__dict__:
            setattr(self.dbObject, key, None)

    def add2(self, name, incoming_timestamp=None, description="", sha256=None, md5=None):
        datpcap = self.dbPcaps.search(name_eq=name)
        if datpcap is not None:
            return False
        self.dbPcaps.id = None
        self.dbPcaps.name = name
        self.dbPcaps.description = description
        if incoming_timestamp is None:
            self.dbPcaps.incoming_timestamp = time.time()
        pathFile = os.papth.join(cfg.PCAP_DIR, name)
        if sha256 is None:
            self.dbPcaps.sha256 = self.sha256Pcap(pathFile)
        if md5 is None:
            self.dbPcaps.md5 = self.md5Pcap(pathFile)
        self.dbPcaps.save()


    def add(self, **kwargs):
        self.uninitTable()

        obj = self.dbObject.search(**kwargs)
        if obj is not None:
            return False
        for key in kwargs:
            setattr(self.dbObject, key, kwargs[key])
        try:
            self.dbObject.save()
        except Exception as e :
            print ("Exception %s in add" % str(e))
            return False
            
        return True

    def delete2(self, pcapId=None, pcapName=None):
        if pcapId is None and pcapName is None:
            return False
        if pcapId is not None:
            self.dbPcaps.delete(pcapId)
        if pcapName is not None:
            pcapsDb = self.dbPcaps.search(name_eq=name)
            if pcapsDb is not None:
                for pcap in pcapsDb:
                    if "id" in pcap:
                        self.pcapsDb.delete(pcap["id"])
                    else:
                        print ("Id not in pcap")
                        print (str(pcap))

    def delete(self, id):
        try:
            self.dbObject.delete(id)
        except Exception as e :
            print ("Exception %s in delete " % str(e))
            return False
        return True

    def get2(self, pcapId=None, pcapName=None):
        if pcapId is None and pcapName is None:
            return False
        if pcapId is not None:
            dbpcap = self.dbPcaps.get(pcapId)
            return dbpcap
        if pcapName is not None:
            dbpcap = self.dbPcaps.search(name_eq=pcapName)
            return dbpcap

    def get(self, id):
        try:
            obj = self.dbObject.get(id)
        except Exception as e:
            print ("Exception %s in get" % str(e))
            return None
        return obj

    def update2(self, id, name=None, md5=None, sha256=None, description=None, incoming_timestamp=None):
        dictAttrs = { "name" : name, "md5" : md5, "sha256" : sha256, "description" : description, "incoming_timestamp": incoming_timestamp }
        pcapDb = self.dbPcaps.search(id_eq=id)
        if pcapDb is not None:
            for key in pcapDb:
                setattr(self.dbPcaps, key, pcapDb[key])
        for key in dictAttrs:
            if dictAttrs[key] is not None:
                self.dbPcaps[key] = dictAttrs[key]
        self.dbPcaps.save()

    def update(self, **kwargs):
        if "id" not in kwargs:
            print ("Id %s not in kwargs" % str(kwargs))
            return False

        self.uninitTable()

        objTable = self.get(kwargs["id"])
        if objTable is None: 
            return False

        for key in objTable:
            setattr(self.dbObject, key, objTable[key])

        for key in kwargs:
            setattr(self.dbObject, key, kwargs[key])

        try: 
            self.dbObject.save()
        except Exception as e:
            print ("Exception at update %s " % str(e))
            return False

        return True

    def getAll2(self, nb, index=0):
        values = self.dbPcaps.getAll(sort="desc", pageNr=index, pageSize=nb)
        return values

    def getAll(self, nb=0, index=0):
        try:
            if nb == 0 and index == 0:
                values = self.dbObject.getAll()
            else:
                values = self.dbPcaps.getAll(sort="desc", pageNr=index, pageSize=nb)
        except Exception as e :
            print ("Exception at getAll")
            return None
        return values
            
        
    def search(self, filterKey, filterValue, comparison="eq"):
        keyWord = "%s_%s" % (filterKey, comparison)
        filters = {keyWord : filterValue}
        values = self.dbObject.search(**filters)
        return values

    def md5Pcap(fname):
        hash_md5 = hashlib.md5()
        try:
            with open(fname, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError:
            return ""

    def sha256Pcap(filename):
        h = hashlib.sha256()
        try:
            with open(filename, 'rb', buffering=0) as f:
                for b in iter(lambda : f.read(128*1024), b''):
                    h.update(b)
            return h.hexdigest()
        except IOError:
            return ""