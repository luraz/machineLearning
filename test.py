link (href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css", rel="stylesheet", id="bootstrap-css")
script (src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js")
script (src="//code.jquery.com/jquery-1.11.1.min.js")
# !------ Include the above in your HEAD tag ----------

# !-- All the files that are required --
link (rel="stylesheet", href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css")
link (href='http://fonts.googleapis.com/css?family=Varela+Round', rel='stylesheet', type='text/css')
script (src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.13.1/jquery.validate.min.js")
meta (name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1")

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
						input (type="text", cls="form-control", id="lg_username", name="lg_username", placeholder="username")
					
					with div (cls="form-group"):
						label ("Password", fr="lg_password", cls="sr-only")
						input (type="password", cls="form-control", id="lg_password", name="lg_password", placeholder="password")
					
					with div (cls="form-group login-group-checkbox"):
						input (type="checkbox", id="lg_remember", name="lg_remember")
						label ("remember", fr="lg_remember")
					
				
				with button (type="submit", cls="login-button"):
					i (cls="fa fa-chevron-right")
			
			with div (cls="etc-login-form"):
				with p("forgot your password?"):
					a ("click here", href="#")
				with p("new user?"): 
					a ("create new account", href="#")
			
	# !-- end:Main Form --


# !-- REGISTRATION FORM --
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
					
					
					# with div cls="form-group login-group-checkbox"
					# 	input type="radio" cls="" name="reg_gender" id="male" placeholder="username"
					# 	label for="male"male/label
						
					# 	input (type="radio" cls="" name="reg_gender" id="female" placeholder="username"
					# 	label ("female", fr="female")
					
					
					with div (cls="form-group login-group-checkbox"):
						input (type="checkbox", cls="", id="reg_agree", name="reg_agree")
						with label ("i agree with", fr="reg_agree"):
							a ("terms", href="#")
					
				with button (type="submit", cls="login-button"):
					i (cls="fa fa-chevron-right")
			
			with div (cls="etc-login-form"):
				with p ("already have an account?"):
				 a ("login here", href="#")
			
	# !-- end:Main Form --


# !-- FORGOT PASSWORD FORM --
with div (cls="text-center", style="padding:50px 0"):
	div ("forgot password", cls="logo")
	# !-- Main Form --
	with div (cls="login-form-1"):
		with form (id="forgot-password-form" cls="text-left"):
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
				with p ("already have an account?"):
					a ("login here", href="#")
				with p ("new user?"): 
					a ("create new account"href="#")
			
	# !-- end:Main Form --