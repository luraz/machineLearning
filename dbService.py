import os

try: 
    from pcapsDatabase import Database as dtb 
    from pcapsDatabase import pcaps
except ImportError:
    print "[ERROR] unable to import from pcapsDatabase pcaps - if.py"

import config as cfg

class dbServicePcaps:
    def __init__(self):
        db = dtb()
        self.dbPcaps = pcaps(db)

    def add(self, name, incoming_timestamp=None, description="", sha256=None, md5=None):
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

    def delete(self, pcapId=None, pcapName=None):
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
                        print "Id not in pcap"
                        print str(pcap)

    def get(self, pcapId=None, pcapName=None):
        if pcapId is None and pcapName is None:
            return False
        if pcapId is not None:
            dbpcap = self.dbPcaps.get(pcapId)
            return dbpcap
        if pcapName is not None:
            dbpcap = self.dbPcaps.search(name_eq=pcapName)
            return dbpcap

    def update(self, id, name=None, md5=None, sha256=None, description=None, incoming_timestamp=None):
        dictAttrs = { "name" : name, "md5" : md5, "sha256" : sha256, "description" : description, "incoming_timestamp": incoming_timestamp }
        pcapDb = self.dbPcaps.search(id_eq=id)
        if pcapDb is not None:
            for key in pcapDb:
                setattr(self.dbPcaps, key, pcapDb[key])
        for key in dictAttrs:
            if dictAttrs[key] is not None:
                self.dbPcaps[key] = dictAttrs[key]
        self.dbPcaps.save()

    def getAll(self, nb, index=0):
        values = self.dbPcaps.getAll(sort="desc", pageNr=index, pageSize=nb)
        return values
        
    def search(self, filterKey, filterValue, comparison="eq"):
        keyWord = "%s_%s" % (filterKey, comparison)
        values = self.dbPcaps.search(**keyWord=filterValue)
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