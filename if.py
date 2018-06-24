import cherrypy
import dominate
from dominate.tags import *
import os
import ast
import shutil
import config as cfg
# from md5 import md5
import time 
from dbService import dbServicePcaps  as dbService

from auth import AuthController, require, member_of, name_is


# class Root:
    
#     _cp_config = {
#         'tools.sessions.on': True,
#         'tools.auth.on': True
#     }
    
#     auth = AuthController()
    
#     restricted = RestrictedArea()
    
#     @cherrypy.expose
#     @require()
#     def index(self):
#         return """This page only requires a valid login."""
    
#     @cherrypy.expose
#     def open(self):
#         return """This page is open to everyone"""
    
#     @cherrypy.expose
#     @require(name_is("joe"))
#     def only_for_joe(self):
#         return """Hello Joe - this page is available to you only"""

#     # This is only available if the user name is joe _and_ he's in group admin
#     @cherrypy.expose
#     @require(name_is("joe"))
#     @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
#     def only_for_joe_admin(self):
#         return """Hello Joe Admin - this page is available to you only"""


# if __name__ == '__main__':
#     cherrypy.quickstart(Root())

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
        # self.dbUsers.add(name="Laura Cirdan", alias="lcirdan", password = "202cb962ac59075b964b07152d234b70", creation_date=time.time(), permission=0)
        
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
        with self.doc:
            with div(cls='container'):
                with div (cls='well well-sm'):
                    h3("Hi", align='center')
        return str(self.doc)

    @cherrypy.expose
    def showSomething(self):
        self.init()
        with self.doc.head:
            with div(cls="well well-sm"):
                h4("hello sucker")
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
                            a("Statistics new Pcap", href="showStatistics")
                        with li():
                            a("Statistics existing Pcap", href="searchStatistics")
                    button("DANGER",cls="btn btn-danger navbar-btn")
                    with ul (cls="nav navbar-nav navbar-right"):
                        with li():
                            with a(href="/auth/register"):
                                # span (" Sign Up", cls="glyphicon glyphicon-user")
                                span("Sign Up")
                        with li():
                            with a (href="#"):

                                # span (cls="glyphicon glyphicon-log-in")
                                span("Login")
        

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
    @require()
    def showStatistics(self,  filename=None, success=False):
        self.init()
        self.showMenu()
        if os.path.isdir(os.path.join(os.getcwd(), "upload")):
            shutil.rmtree(os.path.join(os.getcwd(), "upload"))
        os.makedirs(os.path.join(os.getcwd(), "upload"))
        with self.doc.head:
            if filename is None:
                self.uploadFile()
                if success is not None:
                    if success == True:
                        br();br()
                        with div(id="alertaupload"):
                            div("Success, file uploaded!", cls="alert alert-success")
                
            else:
                filename , extension = os.path.splitext(filename)
                filenamerez = ".".join([filename, "txt"])
                h4(filenamerez)
                filepathresults = os.path.join(cfg.RESULT_DIR, filenamerez)
                if not os.path.isfile(filepathresults):
                    # procesez si creez fisier cu rezultate
                    p("No results . Processing ...")
                    self.processFile(filename)
                    self.showResultsFile(filepathresults)
                else:
                    self.showResultsFile(filepathresults)

        return str(self.doc)

    @cherrypy.expose
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
        return self.showStatistics(success=success, filename=filename)

    def chooseFile(self):
        dictToRepresent = {"name" : "", "sha256" : "", "md5" : "" }
        with self.doc:
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
                self.showResultsFile(filepathresults)
            else:
                self.showResultsFile(filepathresults)



    def showResultsFile(self, filepath):
        f = open(filepath, 'r').read()
        try:
            f = ast.literal_eval(f)
        except Exception as e :
            print ("Could not transform to dict file %s " % str(filepath) )
            print (e)
            return False
        self.representDictionary(f)

    def representDictionary(self ,dictToRepresent, readonly=True):
        with self.doc:
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
        rez = {}
        filename , extension = os.path.splitext(filepath)
        filenamerez = ".".join([filename, "txt"])
        filepathresults = os.path.join(cfg.RESULT_DIR, filenamerez)
        rez["name"] = filename
        rez["nb"] = 1
        rez["56845"] = "afsfsdfs"
        f = open(filepathresults, "w")
        f.write(str(rez))
        f.close()

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
    # cherrypy.quickstart(PcapVisualisation())

if __name__ == '__main__':
    main()