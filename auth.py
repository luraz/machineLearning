import cherrypy
import urllib
from cgi import escape
import md5
import re
import time

import dominate
from dominate.tags import *

try: 
    from pcapsDatabase import Database as dtb 
    from pcapsDatabase import pcaps, users
except ImportError as e:
    print ("[ERROR] unable to import from pcapsDatabase pcaps - if.py %s " % str(e))

SESSION_KEY = '_cp_username'
# import login_and_register as login1
DB = dtb()
DBUSERS = users(DB)

def check_credentials(username, password):
    users = DBUSERS.getAll()
    presumption = 0
    print users
    if users is None:
        return "No users in db"
    for user in users:
        if "username" not in user or "password" not in user:
            continue
        if username == user["username"]:
            presumption = 1
            break
    if presumption == 0:
        return "Incorrect name or password."

    print user['username']
    if md5Function(password) == user["password"]:
        print "here"
        return None

    return "Incorrect name or password."


def md5Function(password):
    m = md5.new()
    m.update(password)
    return m.hexdigest()

def check_auth(*args, **kwargs):
    print "{CHECK AUTH }"
    print str(kwargs)
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as alist of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    
    get_parmas = urllib.quote(cherrypy.request.request_line.split()[1])
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true orfalse
                if not condition():
                    # Send old page as from_page parameter
                    raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" % get_parmas)
        else:
            # Send old page as from_page parameter
            raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" %get_parmas)
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)


def require(*conditions):
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

def member_of(groupname):
    def check():
        user = DBUSERS.search(username_eq=cherrypy.request.login)
        if user is None:
            return False
        if user[0]["role"] == 0:
            return True
        return False
        # return cherrypy.request.login == 'joe' and groupname == 'admin'
    return check

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

def any_of(*conditions):
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

def all_of(*conditions):
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check


class AuthController(object):
    
    def on_login(self, username):
        """Called on successful login"""
    
    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        username=escape(username, True)
        from_page=escape(from_page, True)
        doc = dominate.document(title='Ahahaha')

        # return """htmlbody
        #     form method="post" action="/auth/login"
        #     input type="hidden" name="from_page" value="%(from_page)s" /
        #     %(msg)sbr /
        #     Username: input type="text" name="username" value="%(username)s" /br /
        #     Password: input type="password" name="password" /br /
        #     input type="submit" value="Log in" /
        # /body/html""" % locals()
        with doc.head:
            script (src="//code.jquery.com/jquery-1.11.1.min.js")
            link (href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css", rel="stylesheet", id="bootstrap-css")
            script (src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js")
            
            # !------ Include the above in your HEAD tag ----------

            # !-- All the files that are required --
            link (rel="stylesheet", href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css")
            link (href='http://fonts.googleapis.com/css?family=Varela+Round', rel='stylesheet', type='text/css')
            script (src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.13.1/jquery.validate.min.js")
            meta (name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1")
            link(rel='stylesheet', href='css/style.css')
            script(type='text/javascript', src='js/jquery.js')

            # !-- Where all the magic happens --
            # !-- LOGIN FORM --
            with div (cls="text-center", style="padding:50px 0"):
                div ("login", cls="logo")
                # !-- Main Form --
                with div (cls="login-form-1"):
                    with form (id="login-form", cls="text-left", method='post'):
                        div (cls="login-form-main-message")
                        with div (cls="main-login-form"):
                            with div (cls="login-group"):
                                with div (cls="form-group"):
                                    label ("Username", fr="lg_username", cls="sr-only")
                                    input (type="text", cls="form-control", id="lg_username", name="username", placeholder="username")
                                
                                with div (cls="form-group"):
                                    label ("Password", fr="lg_password", cls="sr-only")
                                    input (type="password", cls="form-control", id="lg_password", name="password", placeholder="password")
                                
                            with button (type="submit", cls="login-button"):
                                i (cls="fa fa-chevron-right")
                        
                        with div (cls="etc-login-form"):
                            # with p("forgot your password?"):
                                # a ("click here", href="#")
                            with p("new user?"): 
                                a ("create new account", href="/auth/register")   
                            with p("not now -> "):
                                a ("home", href="/")   
                        with div(cls="etc-login-form"):
                            p(msg)          

            # !-- FORGOT PASSWORD FORM --
            with div (cls="text-center", style="padding:50px 0"):
                div ("forgot password", cls="logo")
                # !-- Main Form --
                with div (cls="login-form-1"):
                    with form (id="forgot-password-form" ,cls="text-left"):
                        with div (cls="etc-login-form"):
                            p ("When you fill in your registered email address, you will be sent instructions on how to reset your password")
                        
                        div (cls="login-form-main-message")
                        with div (cls="main-login-form"):
                            with div (cls="login-group"):
                                with div (cls="form-group"):
                                    label ("Email address", fr="fp_email", cls="sr-only")
                                    input (type="text", cls="form-control", id="fp_email", name="fp_email", placeholder="email address")
                            
                            with button (type="submit", cls="login-button"):
                                i (cls="fa fa-chevron-right")
                        
                        with div (cls="etc-login-form"):
                            # with p ("already have an account?"):
                                # a ("login here", href="#")
                            with p ("new user?"): 
                                a ("create new account", href="/auth/register")
        return str(doc)
        
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)
        
        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            cherrypy.session.regenerate()
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")
    
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def register(self, **kwargs):
        msg = ""
        if len(kwargs) == 0:
            return self.get_registerform(msg)
       
        error_msg = self.checkUserRegister(**kwargs)
        if error_msg:
            msg = error_msg
        else:
            raise cherrypy.HTTPRedirect("/auth/login")
            
        return self.get_registerform(msg, name=kwargs["name"], username=kwargs["username"], email=kwargs["email"])

    @cherrypy.expose
    def get_registerform(self, msg="", name="", username="", email=""):
        doc = dominate.document(title='Ahahaha')
        with doc.head:
            script (src="//code.jquery.com/jquery-1.11.1.min.js")
            link (href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css", rel="stylesheet", id="bootstrap-css")
            script (src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js")
            link (rel="stylesheet", href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css")
            link (href='http://fonts.googleapis.com/css?family=Varela+Round', rel='stylesheet', type='text/css')
            script (src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.13.1/jquery.validate.min.js")
            meta (name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1")
            link(rel='stylesheet', href='css/style.css')
            script(type='text/javascript', src='js/jquery.js')

            with div (cls="text-center", style="padding:50px 0"):
                div ("register", cls="logo")
                # !-- Main Form --
                with div (cls="login-form-1"):
                    with form (id="register-form", cls="text-left", action="/auth/register", method="post"):
                        div (cls="login-form-main-message")
                        with div (cls="main-login-form"):
                            with div (cls="login-group"):
                                with div (cls="form-group"):
                                    label ("Username", fr="username", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_username", name="username", placeholder="username", value=username)
                                
                                with div (cls="form-group"):
                                    label ("Password", fr="password", cls="sr-only")
                                    input (type="password", cls="form-control", id="reg_password", name="password", placeholder="password")
                                
                                with div (cls="form-group"):
                                    label ("Password Confirm", fr="cpassword", cls="sr-only")
                                    input (type="password", cls="form-control", id="reg_password_confirm", name="cpassword", placeholder="confirm password")
                                
                                
                                with div (cls="form-group"):
                                    label ("Email", fr="reg_email", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_email", name="email", placeholder="email", value=email)
                                
                                with div (cls="form-group"):
                                    label ("Full Name", fr="reg_fullname", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_fullname", name="name", placeholder="full name", value=name)

                                with div (cls="form-group login-group-checkbox"):
                                    input (type="checkbox", cls="", id="reg_agree", name="terms")
                                    with label ("i agree with", fr="reg_agree"):
                                        a ("terms", href="#")
                                
                            with button (type="submit", cls="login-button"):
                                i (cls="fa fa-chevron-right")
                        
                        with div (cls="etc-login-form"):
                            with p ("already have an account?"):
                                a ("login here", href="/auth/login")
                            with p("not now -> "):
                                a ("home", href="/")  
                            p(msg)
        return str(doc)

    @cherrypy.expose
    def checkUserRegister(self, **kwargs):
        if "email" not in kwargs or len(kwargs["email"]) == 0:
            return "Didn't fill out email!"
        if "name" not in kwargs or len(kwargs["name"]) == 0:
            return "Didnt fill out name!"
        if "username" not in kwargs or len(kwargs["username"]) == 0:
            return "Didn't fill out username!"
        if "password" not in kwargs or len(kwargs["password"]) == 0:
            return "Didn't fill out password! "
        if "cpassword" not in kwargs or len(kwargs["cpassword"]) == 0:
            return "Didn't fill out confirm password!"
        if "terms" not in kwargs or len(kwargs["terms"]) == 0:
            return "Read and accept terms and conditions."
        print "fucking kwa"
        print kwargs
        if md5Function(kwargs["password"]) != md5Function(kwargs["cpassword"]):
            return "Password missmatch!"

        users = DBUSERS.getAll()
        if users is not None:
            for user in users:
                if user["username"] == kwargs["username"]:
                    return "Username already exists."

        RX_EMAIL =  re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        mx = RX_EMAIL.search(kwargs["email"])
        if not mx:
            return "Invalid email address"

        DBUSERS.id = None
        DBUSERS.name = kwargs["name"]
        DBUSERS.username = kwargs["username"]
        DBUSERS.email = kwargs["email"]
        DBUSERS.password = md5Function(kwargs["password"])
        DBUSERS.creation_date = time.time()
        DBUSERS.role = 1
        try:
            DBUSERS.save()
        except Exception as e:
            return "Unsuccesful. Please try again later."

        self.sendConfirmationEmail(kwargs["email"], kwargs["username"])

        return None

    def sendConfirmationEmail(self, emailDest, username):
        pass
        # import smtplib

        # # Import the email modules we'll need
        # from email.mime.text import MIMEText

        # # Open a plain text file for reading.  For this example, assume that
        # # the text file contains only ASCII characters.
        # # fp = open(textfile, 'rb')
        # # Create a text/plain message
        # # msg = MIMEText("This is a confirmation email. Your account has been created , %s " % str(username))
        # # fp.close()

        # # me == the sender's email address
        # # you == the recipient's email address
        # # msg['Subject'] = 'Welcome'
        # # msg['From'] = "cirdan.laura1@gmail.com"
        # # msg['To'] = emailDest

        # # Send the message via our own SMTP server, but don't include the
        # # envelope header.
        #     # s = smtplib.SMTP('localhost')
        #     # s.sendmail(me, [you], msg.as_string())
        #     # s.quit()
        # import smtplib
        # pwd = "testaccount"
        # FROM = "lauraandreeacirdan@gmail.com"
        # TO = emailDest
        # SUBJECT = "Confirmation"
        # TEXT = "This is a confirmation email. Your account has been created , %s " % str(username)

        # # Prepare actual message
        # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        # """ % (FROM, TO, SUBJECT, TEXT)
        # try:
        #     server = smtplib.SMTP("smtp.gmail.com", 587)
        #     server.ehlo()
        #     server.starttls()
        #     server.login(FROM, pwd)
        #     server.sendmail(FROM, TO, message)
        #     server.close()
        #     print 'successfully sent the mail'
        # except Exception as e :
        #     print "failed to send mail %s " % str(e)


