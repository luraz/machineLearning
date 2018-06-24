import cherrypy
import urllib
from cgi import escape

import dominate
from dominate.tags import *

SESSION_KEY = '_cp_username'
import login_and_register as login1

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
    print "{CHECK AUTH }"
    print str(kwargs)
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
    #     return """htmlbody
    #         form method="post" action="/auth/login"
    #         input type="hidden" name="from_page" value="%(from_page)s" /
    #         %(msg)sbr /
    #         Username: input type="text" name="username" value="%(username)s" /br /
    #         Password: input type="password" name="password" /br /
    #         input type="submit" value="Log in" /
    #     /body/html""" % locals()

    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        username=escape(username, True)
        from_page=escape(from_page, True)
        doc = dominate.document(title='Ahahaha')

        # l = LoginForm()
        # loginform  = l.loginAndRehistrate()
        # return loginform
        # loginform = login1.loginAndregister(username, from_page=from_page, msg=msg)
        # return loginform

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
                    with form (id="login-form", cls="text-left"):
                        div (cls="login-form-main-message")
                        with div (cls="main-login-form"):
                            with div (cls="login-group"):
                                with div (cls="form-group"):
                                    label ("Username", fr="lg_username", cls="sr-only")
                                    input (type="text", cls="form-control", id="lg_username", name="username", placeholder="username")
                                
                                with div (cls="form-group"):
                                    label ("Password", fr="lg_password", cls="sr-only")
                                    input (type="password", cls="form-control", id="lg_password", name="password", placeholder="password")
                                
                                with div (cls="form-group login-group-checkbox"):
                                    input (type="checkbox", id="lg_remember", name="lg_remember")
                                    label ("remember", fr="lg_remember")
                                
                            
                            with button (type="submit", cls="login-button"):
                                i (cls="fa fa-chevron-right")
                        
                        with div (cls="etc-login-form"):
                            # with p("forgot your password?"):
                                # a ("click here", href="#")
                            with p("new user?"): 
                                a ("create new account", href="/auth/register")
                        
                # !-- end:Main Form --


            # # !-- REGISTRATION FORM --
            # with div (cls="text-center", style="padding:50px 0"):
            #     div ("register", cls="logo")
            #     # !-- Main Form --
            #     with div (cls="login-form-1"):
            #         with form (id="register-form", cls="text-left"):
            #             div (cls="login-form-main-message")
            #             with div (cls="main-login-form"):
            #                 with div (cls="login-group"):
            #                     with div (cls="form-group"):
            #                         label ("Email address", fr="reg_username", cls="sr-only")
            #                         input (type="text", cls="form-control", id="reg_username", name="reg_username", placeholder="username")
                                
            #                     with div (cls="form-group"):
            #                         label ("Password", fr="reg_password", cls="sr-only")
            #                         input (type="password", cls="form-control", id="reg_password", name="reg_password", placeholder="password")
                                
            #                     with div (cls="form-group"):
            #                         label ("Password Confirm", fr="reg_password_confirm", cls="sr-only")
            #                         input (type="password", cls="form-control", id="reg_password_confirm", name="reg_password_confirm", placeholder="confirm password")
                                
                                
            #                     with div (cls="form-group"):
            #                         label ("Email", fr="reg_email", cls="sr-only")
            #                         input (type="text", cls="form-control", id="reg_email", name="reg_email", placeholder="email")
                                
            #                     with div (cls="form-group"):
            #                         label ("Full Name", fr="reg_fullname", cls="sr-only")
            #                         input (type="text", cls="form-control", id="reg_fullname", name="reg_fullname", placeholder="full name")
                                
                                
            #                     # with div cls="form-group login-group-checkbox"
            #                     #   input type="radio" cls="" name="reg_gender" id="male" placeholder="username"
            #                     #   label for="male"male/label
                                    
            #                     #   input (type="radio" cls="" name="reg_gender" id="female" placeholder="username"
            #                     #   label ("female", fr="female")
                                
                                
            #                     with div (cls="form-group login-group-checkbox"):
            #                         input (type="checkbox", cls="", id="reg_agree", name="reg_agree")
            #                         with label ("i agree with", fr="reg_agree"):
            #                             a ("terms", href="#")
                                
            #                 with button (type="submit", cls="login-button"):
            #                     i (cls="fa fa-chevron-right")
                        
            #             with div (cls="etc-login-form"):
            #                 with p ("already have an account?"):
            #                  a ("login here", href="#")
                        
            #     # !-- end:Main Form --


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
    def register(self):
        # !-- REGISTRATION FORM --
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
                    with form (id="register-form", cls="text-left"):
                        div (cls="login-form-main-message")
                        with div (cls="main-login-form"):
                            with div (cls="login-group"):
                                with div (cls="form-group"):
                                    label ("Email address", fr="reg_username", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_username", name="reg_username", placeholder="username")
                                
                                with div (cls="form-group"):
                                    label ("Password", fr="reg_password", cls="sr-only")
                                    input (type="password", cls="form-control", id="reg_password", name="reg_password", placeholder="password")
                                
                                with div (cls="form-group"):
                                    label ("Password Confirm", fr="reg_password_confirm", cls="sr-only")
                                    input (type="password", cls="form-control", id="reg_password_confirm", name="reg_password_confirm", placeholder="confirm password")
                                
                                
                                with div (cls="form-group"):
                                    label ("Email", fr="reg_email", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_email", name="reg_email", placeholder="email")
                                
                                with div (cls="form-group"):
                                    label ("Full Name", fr="reg_fullname", cls="sr-only")
                                    input (type="text", cls="form-control", id="reg_fullname", name="reg_fullname", placeholder="full name")

                                with div (cls="form-group login-group-checkbox"):
                                    input (type="checkbox", cls="", id="reg_agree", name="reg_agree")
                                    with label ("i agree with", fr="reg_agree"):
                                        a ("terms", href="#")
                                
                            with button (type="submit", cls="login-button"):
                                i (cls="fa fa-chevron-right")
                        
                        with div (cls="etc-login-form"):
                            with p ("already have an account?"):
                             a ("login here", href="/auth/login")
        return str(doc)
