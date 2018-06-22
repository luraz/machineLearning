import cherrypy
import urllib
from cgi import escape

SESSION_KEY = '_cp_username'

def check_credentials(username, password):
    if username in ('joe', 'steve') and password == 'secret':
        return None
    else:
        return u"Incorrect username or password."
    
# def check_auth(*args, **kwargs):
#     conditions = cherrypy.request.config.get('auth.require', None)
#     if conditions is not None:
#         username = cherrypy.session.get(SESSION_KEY)
#         if username:
#             cherrypy.request.login = username
#             for condition in conditions:
#                 # A condition is just a callable that returns true or false
#                 if not condition():
#                     raise cherrypy.HTTPRedirect("/auth/login")
#         else:
#             raise cherrypy.HTTPRedirect("/auth/login")

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as alist of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    # format GET params
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
        return cherrypy.request.login == 'joe' and groupname == 'admin'
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
    
    # def get_loginform(self, username, msg="Enter login information", from_page="/"):
    #     return """<html><body>
    #         <form method="post" action="/auth/login">
    #         <input type="hidden" name="from_page" value="%(from_page)s" />
    #         %(msg)s<br />
    #         Username: <input type="text" name="username" value="%(username)s" /><br />
    #         Password: <input type="password" name="password" /><br />
    #         <input type="submit" value="Log in" />
    #     </body></html>""" % locals()

    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        username=escape(username, True)
        from_page=escape(from_page, True)
        return """<html><body>
            <form method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br />
            Username: <input type="text" name="username" value="%(username)s" /><br />
            Password: <input type="password" name="password" /><br />
            <input type="submit" value="Log in" />
        </body></html>""" % locals()

        # with self.doc:
        #     with form(method="post", action="/auth/login"):
        #         input(type="hidden", name="from_page", value="%(from_page)s"  %(msg))
        #         br()
        #         label("username")
        #         input(type="text", name="username", value="%(username)s" )
        #         label("password")
        #         input(type="password", name="password")
        #         input(type='submit', value="Log in")
    
    # @cherrypy.expose
    # def login(self, username=None, password=None, from_page="/"):
    #     if username is None or password is None:
    #         return self.get_loginform("", from_page=from_page)
        
    #     error_msg = check_credentials(username, password)
    #     if error_msg:
    #         return self.get_loginform(username, error_msg, from_page)
    #     else:
    #         cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
    #         self.on_login(username)
    #         raise cherrypy.HTTPRedirect(from_page or "/")

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