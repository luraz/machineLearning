import cherrypy
import dominate
from dominate.tags import *
import os
import ast
import shutil
import config as cfg
import subprocess
import ntpath
import shlex
from bs4 import BeautifulSoup
# from md5 import md5
import time 
from dbService import dbServicePcaps  as dbService

from auth import AuthController, require, member_of, name_is

ROLES = {
    0 : 'administator', 
    1 : 'standard'
}

SESSION_KEY = '_cp_username'

class PcapVisualisationAdmin:
    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index(self):
        self.init()
        self.showMenu()
        # self.showChosenFile()
        return str(self.doc)

    def init(self):
        self.doc = dominate.document(title='Ahahaha')
        with self.doc.head:
            link(rel='stylesheet', href='css/style.css')
            link(rel='stylesheet', href='css/bootstrap.min.css')
            
            script(type='text/javascript', src='js/jquery.js')
            script(type='text/javascript', src="js/three.js")
            script(type='text/javascript', src="js/Projector.js")
            script(type='text/javascript', src="js/CanvasRenderer.js")
            script(type='text/javascript', src="js/OrbitControls.js")
            script(type='text/javascript', src='js/bootstrap.min.js')
            script(type='text/javascript', src='js/script.js')

    def showMenu(self):
        with self.doc.head:
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0")
            with nav(cls="navbar navbar-inverse"):
                with div(cls="container-fluid"):
                    with div(cls="navbar-header"):
                        a("HOME",cls="navbar-brand", href="/home")
                    with ul(cls="nav navbar-nav"):
                        with li():
                            a("Player", href="/")
                        with li():
                            a("Statistics new Pcap", href="showStatistics")
                        with li():
                            a("Statistics existing Pcap", href="searchStatistics")
                    button("DANGER",cls="btn btn-danger navbar-btn")

class PcapVisualisation:
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }
    
    auth = AuthController()
    
    restricted = PcapVisualisationAdmin()

    def __init__(self):
        
        self.dbPcaps = dbService("pcaps")
        self.dbUsers = dbService("users")
        
    def init(self):
        self.doc = dominate.document(title='Ahahaha')
        with self.doc.head:
            link(rel='stylesheet', href='css/style.css')
            link(rel='stylesheet', href='css/bootstrap.min.css')
            
            script(type='text/javascript', src='js/jquery.js')
            script(type='text/javascript', src="js/three.js")
            script(type='text/javascript', src="js/Projector.js")
            script(type='text/javascript', src="js/CanvasRenderer.js")
            script(type='text/javascript', src="js/OrbitControls.js")
            script(type='text/javascript', src='js/bootstrap.min.js')
            script(type='text/javascript', src='js/script.js')
            
    @cherrypy.expose
    # @require()
    def index(self):
        # self.init()
        # self.showMenu()
        # self.showChosenFile()
        self.home()
        return str(self.doc)

    @cherrypy.expose
    # @require()
    def home(self):
        self.init()
        self.showMenu()
        username = cherrypy.session.get(SESSION_KEY)
        with self.doc:
            with div(cls='container'):
                with div (cls='well well-sm'):
                    if str(username) != "None":
                        h3("Hi, %s" % username, align='center')
                    else:
                        h3("Hi", align='center')
        return str(self.doc)

    def showMenu(self):
        with self.doc.head:
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0")
            with nav(cls="navbar navbar-inverse"):
                with div(cls="container-fluid"):
                    with div(cls="navbar-header"):
                        a("HOME",cls="navbar-brand", href="/home")
                    with ul(cls="nav navbar-nav"):
                        with li():
                            a("Player", href="/player")
                        with li():
                            a("Statistics", href="/statistics")
                        # with li():
                            # a("Statistics existing Pcap", href="searchStatistics")
                    # button("DANGER",cls="btn btn-danger navbar-btn")
                    username = cherrypy.session.get(SESSION_KEY)
                    print username
                    with ul (cls="nav navbar-nav navbar-right"):
                        if username is None or str(username) == "None":
                            with li():
                                with a(href="/auth/register"):
                                    # span (" Sign Up", cls="glyphicon glyphicon-user")
                                    span("Sign Up")
                            with li():
                                with a (href="/auth/login"):

                                    # span (cls="glyphicon glyphicon-log-in")
                                    span("Login")
                        else:
                            with li():
                                with a(href="/auth/logout"):
                                    span("Log out")
        

    # @cherrypy.expose
    # @require()
    # @require(member_of("administrator")) 
    # def editUsers(self, **kwargs):
    #     self.init()
    #     self.showMenu()
    #     nb = 0
    #     index = 0
    #     if "nb" in kwargs:
    #         nb = kwargs["nb"]
    #     if index in kwargs:
    #         index = kwargs["index"]

    #     values = self.dbUsers.getAll()



    #     with self.doc:
    #         with div (cls="container"):
    #           with ul (cls="pagination"):
    #             with li():
    #                 a ("1", href="#")
    #             with li(cls="active"):
    #                 a ("2", href="#")
    #             with li():
    #                 a ("3", href="#")
    #             with li():
    #                 a ("4", href="#")
    #             with li():
    #                 a ("5", href="#")
    #     return str(self.doc)


    @cherrypy.expose
    @require()
    def player(self, filename=None):
        self.init()
        self.showMenu()
        filename = "a.pcap"
        with self.doc:
            with div(cls='well well-sm'):
                if filename is None:
                    p("No file loaded")
                else :
                    span(str(filename))
                    button("Play", cls='btn',id="plyerlink")
        return str(self.doc)

    @cherrypy.expose
    # @require()
    def statistics(self, success=False, filename=None):
        self.init()
        self.showMenu()
        rez = None
        with self.doc:
            with div(cls='well well-sm'):
                a("Upload File", cls="btn btn-primary", data_toggle="collapse", href="#collapseExample", role="button", aria_expanded="false", aria_controls="collapseExample")
                with div():
                    br()
                    with div (cls="collapse", id="collapseExample"):
                        with div (cls="card card-body"):
                            self.showStatistics()
  
            with div(cls="well well-sm"):
                a("Search File", cls="btn btn-primary", data_toggle="collapse", href="#collapseExample2", role="button", aria_expanded="false", aria_controls="collapseExample2")

                with div():
                    br()
                    with div (cls="collapse", id="collapseExample2"):
                        with div (cls="card card-body"):
                            self.chooseFile()

            if success:
                # filename , extension = os.path.splitext(filename)
                # filenamerez = ".".join([filename, "txt"])
                # h4(filenamerez)
                filepathresults = os.path.join(cfg.RESULT_DIR, filename, "index.html")
                if not os.path.isfile(filepathresults):
                    # procesez si creez fisier cu rezultate
                    p("No results . Processing ...")
                    self.processFile(filename)
                    rez = self.showResultsFile(filename)
                else:
                    rez = self.showResultsFile(filename)

        if rez is None:
            return str(self.doc)
        return rez

    @cherrypy.expose
    @require()
    def showStatistics(self,  filename=None, success=False):
        # self.init()
        # self.showMenu()
        if os.path.isdir(os.path.join(os.getcwd(), "upload")):
            shutil.rmtree(os.path.join(os.getcwd(), "upload"))
        os.makedirs(os.path.join(os.getcwd(), "upload"))
        # with self.doc:
        if filename is None:
            self.uploadFile()
            if success is not None:
                if success == True:
                    br();br()
                    with div(id="alertaupload"):
                        div("Success, file uploaded!", cls="alert alert-success")
            
        else:
            # filename , extension = os.path.splitext(filename)
            # filenamerez = ".".join([filename, "txt"])
            # h4(filenamerez)
            filepathresults = os.path.join(cfg.RESULT_DIR, filename, "index.html")
            if not os.path.isfile(filepathresults):
                # procesez si creez fisier cu rezultate
                p("No results . Processing ...")
                pathResults = self.processFile(filename)
                if not pathResults:
                    self.showFileErrorMessage(filename)
                self.showResultsFile(filename)
            else:
                self.showResultsFile(filename)

        # return str(self.doc)

    @cherrypy.expose
    def showFileErrorMessage(self, filename):
        with div(cls="well well-sm"):
            h4("No results for file %s" % ntpath.basename(filename))

    @cherrypy.expose
    @require()
    def searchStatistics(self):
        self.init()
        self.showMenu()
        self.chooseFile()
        return str(self.doc)

    @cherrypy.expose
    def uploadFile(self, success=None):
        uploadedFile = False
        uploadFolder = os.path.join(os.getcwd(), "upload")
        if os.path.isdir(uploadFolder):
            if len(os.listdir(uploadFolder)) == 1:
                uploadedFile = True
                filee = os.listdir(uploadFolder)[0]
        br()
        with form(id="uploadForm",action="uploadRedirect",  method="post", enctype="multipart/form-data", cls='form-horizontal'):
            with div (cls="input-group"):
                with label (cls="input-group-btn"):
                    with span("Browse", cls="btn btn-primary"):
                        input (type="file", style="display: none;",name="myFile")
                with div(cls='col-sm-3'):
                    if uploadedFile:
                        print ("neh")
                        input (value=filee, type="text", cls="form-control", readonly="readonly")
                    else:
                        print ("yes")
                        input (type="text", cls="form-control", readonly="readonly")
            br()
            input(value="Upload", type="submit", cls='btn')
            

    def upload(self, myFile):
        if os.path.isdir(os.path.join(os.getcwd(), "upload")):
            shutil.rmtree(os.path.join(os.getcwd(), "upload"))
        os.makedirs(os.path.join(os.getcwd(), "upload"))
        if len(myFile.filename) == 0:
            return None
        dest = os.path.join(os.getcwd(), "upload", myFile.filename)
        size = 0
        f = open(dest, "w")
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            f.write(data)
            size += len(data)
        f.close()
        return dest

    @cherrypy.expose
    def uploadRedirect(self, **kwargs):
        if "myFile" in kwargs:
            myFile = kwargs["myFile"]
        else:
            myFile = None
        success = False
        filename = None
        rez = self.upload(myFile)
        filename = kwargs["myFile"].filename
        if rez is not None:
            success = True
        if len(filename) == 0:
            filename = None
        raise cherrypy.HTTPRedirect("/statistics?success=%s&filename=%s" % (success, filename))
        # return self.statistics(success=success, filename=filename)

    def chooseFile(self):
        dictToRepresent = {"name" : "", "sha256" : "", "md5" : "" }
        # with self.doc:
        with form(action="/filterResults"):
            self.representDictionaryAsComboBox(dictToRepresent, readonly=False, givenid="searchFileCombobox", givenidInput="searchFileInput")
            br()
            with div(cls='container'):        
                button("Search pcap", cls="btn", id="seachPcapBTN", type="submit")

    @cherrypy.expose
    def filterResults(self, filterName, filterValue ):
        pass
        results = self.dbPcaps.search(filterName, filterValue)
        if results is None:
            pass
            raise cherrypy.HTTPRedirect("/statistics")
        else:
            if len(results) != 1:
                pass
                # error len pcaps is not 0
            # for pcap in results:
            pcap = results[0]
            if "name" not in pcap:
                pass
                # error - no filename
            filename = pcap["name"]
            filename , extension = os.path.splitext(filename)
            filenamerez = ".".join([filename, "txt"])
            h4(filenamerez)
            filepathresults = os.path.join(cfg.RESULT_DIR, filenamerez)
            if not os.path.isfile(filepathresults):
                # procesez si creez fisier cu rezultate
                p("No results . Processing ...")
                self.processFile(filename)
            success = True

            raise cherrypy.HTTPRedirect("/statistics?success=%s&filename=%s" % (success, filename))
                # self.showResultsFile(filepathresults)

    def showResultsFile(self, filename):
        # filename = ntpath.basename(filepath)
        pathfileResults = os.path.join(cfg.RESULT_DIR, filename, "index.html")
        if not os.path.isfile(pathfileResults):
            self.showFileErrorMessage(filename)

        self.init()
        self.showMenu()
        with self.doc:
            with div(cls="well well-lg"):
                    h3("File: %s" % str(filename))
            with div(cls="container"):
                with div(cls="well well-sm"):
                    a("TCP/UDP Sessions", href="showResultsFileSession?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("IP Count", href="showResultsFileIpCount?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("TCP Port Count", href="showResultsFileTCPPortCount?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("TCP Port Count", href="showResultsFileUDPPortCount?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("IP Protocol Count", href="showResultsFileIpProtocolCount?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("Ethernet Type Count", href="showResultsFileEthTypeCount?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("Image Report", href="showResultsFileImageReport?filename=%s" %filename)
                with div(cls="well well-sm"):
                    a("GET/POST Report", href="showResultsFileGetPostReport?filename=%s" % filename)
                with div(cls="well well-sm"):
                    a("HTTP Proxy Log", href="showResultsFileHttpProxylog?filename=%s" % filename)

    def getBootstrapInclude(self):
        return  """
        <html><head>
        <title>Ahahaha</title>

        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        </head><body>
        """

    def divideIndex(self, filename):
        #divide in : TCP/UDP sessions, IP count, TCP Port Count, IP Protocol Count, Ethernet Type Count

        if filename is None:
            print "none"
            return "FilePath is None"
        # if not os.path.isfile(filename):
        #     print "not a file"
        #     return "File Path not a file %s" % str(filename)
        pathIndex = os.path.join(cfg.RESULT_DIR, filename, "index.html")
        if not os.path.isfile(pathIndex):
            print "index"
            return "Path index not a file %s" % str(pathIndex)
        f = open(pathIndex, "r").read()
        soup = BeautifulSoup(f, "html.parser")
        a = soup.find_all("table")
        counter = 0
        for tableContent in a :
            pathTable = os.path.join(cfg.RESULT_DIR, filename, "%d.html" % counter)
            fw = open(pathTable, "w")
            fw.write(str(tableContent))
            fw.close()
            counter += 1


        # for tableName in ["image.html", "getpost.html", "httplog.text"]:
        tableName = "image.html"
        pathTable = os.path.join(cfg.RESULT_DIR, filename, tableName)
        newPathTable = os.path.join(cfg.RESULT_DIR, filename, "%d.html" % counter)
        f = open(pathTable, "r")
        soup = BeautifulSoup(f, "html.parser")
        a = soup.find_all("table")
        fw = open(newPathTable, "w")
        fw.write(str(a[0]))
        fw.close()
        f.close()
        counter += 1

        tableName = "getpost.html"
        newContent = ""
        pathTable = os.path.join(cfg.RESULT_DIR, filename, tableName)
        newPathTable =  os.path.join(cfg.RESULT_DIR, filename, "%d.html" % counter)
        f = open(pathTable, "r")
        line = f.readline()
        while "HTTP GETs and POSTs" not in line:
            line = f.readline()

        while line:
            newContent += line
            line = f.readline()

        f.close()
        f = open(newPathTable, "w")
        f.write(newContent)
        f.close()
            
        counter += 1

        tableName = "httplog.text"
        pathTable = os.path.join(cfg.RESULT_DIR, filename, tableName)
        newPathTable =  os.path.join(cfg.RESULT_DIR, filename, "%d.html" % counter)
        f = open(pathTable)
        content = f.read()
        f.close()
        content.replace("\n", "<br>")
        f = open(newPathTable, "w")
        f.write(content)
        f.close()


    @cherrypy.expose
    def showResultsFileSession(self, filename):
        TABLE_NUMBER = 0
        tableHeads = """
                <tr><th>Nb</th>
                <th>Date</th>
                <th>Seconds</th>
                <th>IP Src</th>
                <th>Type</th>
                <th>Bytes</th>
                <th>Session</th>
                </tr>
                """
        Tabletitle = "TCP/UDP Sessions"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileIpCount(self, filename):
        TABLE_NUMBER = 1
        tableHeads = """
                <tr>
                    <th>IP</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "IP Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileTCPPortCount(self, filename):
        TABLE_NUMBER = 2
        tableHeads = """
                <tr>
                    <th>Port</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "TCP Port Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileUDPPortCount(self, filename):
        TABLE_NUMBER = 3
        tableHeads = """
                <tr>
                    <th>Port</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "UDP Port Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileIpProtocolCount(self, filename):
        TABLE_NUMBER = 4
        tableHeads = """
                <tr>
                    <th>Protocol</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "IP Protocol Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileEthTypeCount(self, filename):
        TABLE_NUMBER = 5
        tableHeads = """
                <tr>
                    <th>Ethernet Type</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "Ethernet Type Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileImageReport(self, filename):
        TABLE_NUMBER = 6
        tableHeads = """
                <tr>
                    <th>Nb</th>
                    <th>Date</th>
                    <th>Corresponded IPS</th>
                    <th>Image</th>
                </tr>
                """
        Tabletitle = "Images"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileGetPostReport(self, filename):
        TABLE_NUMBER = 7
        tableHeads = ""
                # <tr>
                #     <th>Nb</th>
                #     <th>Date</th>
                #     <th>Method</th>
                #     <th>Details</th>
                # </tr>
                # """
        Tabletitle = ""
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    @cherrypy.expose
    def showResultsFileHttpProxylog(self, filename):
        TABLE_NUMBER = 8
        tableHeads = """
                <tr>
                    <th>IP</th>
                    <th>Count</th>
                </tr>
                """
        Tabletitle = "IP Count"
        result = self.getHtmlTable(filename, TABLE_NUMBER, tableHeads, Tabletitle)
        return result

    def getHtmlTable(self, filename, TABLE_NUMBER, tableHeads, Tabletitle):
        tableName = "%d.html" % TABLE_NUMBER
       
        pathfileResults = os.path.join(cfg.RESULT_DIR, filename, tableName)
        if not os.path.isfile(pathfileResults):
            self.divideIndex(filename)
        try:
            f = open(pathfileResults, "r")
        except OSError:
            self.showFileErrorMessage(filename)
            print "Error on showResultsFileIpCount %s" % str(filename)
            return ""

        newResult = self.getBootstrapInclude()
        linee = "<div class='well well-sm'><h3> %s </h3></div>" % str(Tabletitle)
        while linee:
            linee = linee.replace("blue", "#008B8B")
            linee = linee.replace("red", "#B8860B")
            linee = linee.replace("<table", '<table class="table table-hover" ')
            linee = linee.replace("border=2", "")
            if "<table" in linee:
                newResult += linee
                newResult +=  tableHeads               
            else:
                newResult += linee
            linee  = f.readline()
        return newResult

    def representDictionary(self ,dictToRepresent, readonly=True):
        # with self.doc:
        with div(cls='container'):
            with form(cls="form-horizontal"):
                with div(cls='form-group'):
                    for key in sorted(dictToRepresent):
                        label(key, cls="col-sm-2 control-label")
                        with div(cls="col-sm-10"):
                            if readonly:
                                input(str(dictToRepresent[key]),value=dictToRepresent[key], cls='form-control',readonly="readonly", id=str(key) ,name="inputdictionary", maxlength=250)
                            else:
                                input(str(dictToRepresent[key]),value=dictToRepresent[key], cls='form-control', id=str(key), name="inputdictionary", maxlength=250)

    def representDictionaryAsComboBox(self, dictToRepresent, readonly=True, givenid="comboboxDefaultId", givenidInput="inputDefaultId"):
        with div(cls='col-sm-3'):
            with select(cls='combobox  form-control col-sm-4', align="left", id=givenid, name="filterName"):
                for key in sorted(dictToRepresent):
                    option ( str(key), value=str(key))
            input (cls="form-control" , type="text", id=givenidInput, pattern=".{3,}",required="required",  title="3 characters minimum", name="filterValue")


    def processFile(self, filepath):
        filename = ntpath.basename(filepath)
        pathFileIndexRezults = os.path.join(cfg.RESULT_DIR,filename, "index.html")
        if os.path.exists(pathFileIndexRezults):
            return pathFileIndexRezults
        currentPath = os.getcwd()
        pathResults = os.path.join(cfg.RESULT_DIR, filename)
        if not os.path.exists(pathResults):
            os.makedirs(pathResults)
        shutil.copy(os.path.join(os.getcwd(), "chaosreader0.94"), pathResults)
        os.chdir(pathResults)
        cmd = "perl chaosreader0.94 %s" % filepath
        print cmd
        try:
            p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except Exception as e:
            os.chdir(currentPath)
            print "Could not process file with error %s " % str(e)
            return False

        os.chdir(currentPath)
        
        if os.path.isfile(pathFileIndexRezults):
            return pathFileIndexRezults
        return False


def getUsers():
    dbUsers = dbService("users")
    userss = dbUsers.getAll()
    return userss

# def encryptPassword(pw):
#     return md5(pw).hexdigest()

def main():
    # [/]
# tools.staticdir.root = "L:\\workspace/licenta/machineLearning/"
# tools.staticfile.root = "L:\\workspace/licenta/machineLearning/"

    # users = getUsers()

    # cherrypy.config.update({'/secure': {'tools.basic_auth.on': True,
    #                     'tools.basic_auth.realm': 'Some site2',
    #                     'tools.basic_auth.users': users,
    #                     'tools.basic_auth.encrypt': encryptPassword}})
    # root = PcapVisualisationPublic()
    # root.secure = PcapVisualisation()
    # cherrypy.quickstart(PcapVisualisation, '/', 'a.conf')
    # cherrypy.config.update({'/' : {
    #         'tools.staticdir.root' : os.getcwd(),
    #         'tools.staticfile.root' : os.getcwd()
    #     }})
    cherrypy.quickstart(PcapVisualisation(), '/', 'a.conf')


    # p = PcapVisualisation()
    # p.divideIndex("/home/laura/games/pcaps/97bfbdd66c14c4fd94637c2c3d2b6419ddbac8f6425ef5e8a941a98ff3b4c52d")
    # p.processFile("/home/laura/games/pcaps/97bfbdd66c14c4fd94637c2c3d2b6419ddbac8f6425ef5e8a941a98ff3b4c52d")

if __name__ == '__main__':
    main()