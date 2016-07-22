"""
Start of final project for Software Projects.

I took some time and got together what I think we can work with. It is an environment with Python, using WebApp2, and Jinja2 for templating
The webserver part is not as robust as I would like, sometimes I need to stop and start it when it gets various errors. There are two key Python files. 

main.py and api.py. 

"""	

import webapp2
import jinja2
from jinja2 import Environment, PackageLoader
import os
import mysql.connector
import json
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText as text
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders

import subprocess
from webapp2_extras import sessions

dbName = 'lambda'
dbUser = 'student'
dbPass = 'default'
dbHost = 'localhost'

emailUser = 'certifcatecenter@gmail.com'
emailPass = 'CapStone16'

#Create database connection and cursor for queries
cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
cursor = cnx.cursor(buffered=True)

#loggedIn will check to see if the user is logged in yet
#being loggedIn depends on whether the browser has user as a session variable
def loggedIn(handler):
    def checkLogin(self):
        #if the user is logged in, then return the appropriate handler
        if 'user' in self.session:
            return handler(self)
        #if the user is not logged in, then redirect to the sign in page
        else:
            self.redirect("index.html")

    return checkLogin


"""
BaseHandler code below is from the webapp2 sessions official documentation
Code from http://webapp2.readthedocs.io/en/latest/api/webapp2_extras/sessions.html
"""
class BaseHandler(webapp2.RequestHandler):
        def dispatch(self):
            self.session_store = sessions.get_store(request=self.request)

            try:
                webapp2.RequestHandler.dispatch(self)
            finally:
                self.session_store.save_sessions(self.response)

        @webapp2.cached_property
        def session(self):
            return self.session_store.get_session()


class SignOnPage(BaseHandler):
	def get(self):
            #if the user is already logged in, then redirect to the dashboard page
                if 'user' in self.session:
                    self.redirect("dashboard.html")
                else:
		    env = Environment(loader=PackageLoader('api', '/templates'))
		    template = env.get_template('index.html')
		    self.response.out.write(template.render())

	def post(self):
		out_obj = {}

		out_obj = {'msg': 'Success, Your POST worked!'}
		self.response.out.write(json.dumps(out_obj))

class AboutPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('about.html')
		self.response.out.write(template.render())

class DashboardPage(BaseHandler):
        @loggedIn
        def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('dashboard.html')
		self.response.out.write(template.render())

class UsersPage(BaseHandler):
        @loggedIn
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('users.html')
		self.response.out.write(template.render())

class ExistingPage(BaseHandler):
        @loggedIn
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('existing.html')
		self.response.out.write(template.render())

class SignUpPage(BaseHandler):
        def get(self):
	        if 'user' in self.session:
                    self.redirect("dashboard.html")
                else:
                    env = Environment(loader=PackageLoader('api', '/templates'))
		    template = env.get_template('signUp.html')
		    self.response.out.write(template.render())

class AccountPage(BaseHandler):
        @loggedIn
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('account.html')
		self.response.out.write(template.render())

class ForgetPasswordPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('forget.html')
		self.response.out.write(template.render())

class CheckLogin(BaseHandler):
	def post(self):
		#Simple example of login validation to show mysql connector syntax
		validLogin = False
		#Assume the sign on page POSTS a username and password
		username = self.request.get('email', default_value=None)
		password = self.request.get('password', default_value=None)
		hashedPass = hashlib.sha1(password).hexdigest();
		#(1)Create the MySQL command, (2)Execute it
		userQuery = ("SELECT password FROM users WHERE email = '"+username+"'")
		cursor.execute(userQuery)
		passwordQuery = cursor.fetchone()
		#Check entered password against user's stored password
		if passwordQuery != None:
			passwordInDb = passwordQuery[0].encode('utf-8')
			if passwordInDb == hashedPass:
                                #get user ID from the database to add to sessions
                                idQuery = ("SELECT id FROM users WHERE email = '"+username+"'")
                                cursor.execute(idQuery)
                                idValue = cursor.fetchone()
                                #set the session value for user
                                self.session['user'] = idValue
				self.redirect("/dashboard.html")
		outMsg = {"message" : "Invalid login credentials. Please try again."}
		self.response.out.write(json.dumps(outMsg))


class CreateUserAccount(webapp2.RequestHandler):
	def post(self):
		postData = json.loads(self.request.body)
		username = postData['email']
		fName = postData['firstName']
		lName = postData['lastName']
		name = fName + " " + lName
		password = postData['password']
		signature = "haven't figured this out yet"
		instant = datetime.datetime.now()

		usernameTakenTest = ("SELECT * FROM users WHERE email = '"+username+"'")
		cursor.execute(usernameTakenTest)

		testResult = cursor.fetchone()
		#Username is available
		if testResult == None:
			hashedPass = hashlib.sha1(password).hexdigest()
			userDetails = (name, username, hashedPass, instant, signature)
			userInsert = ("INSERT INTO users (name, email, password, dateCreated, signature) VALUES (%s, %s, %s, %s, %s)")
			cursor.execute(userInsert, userDetails)
			#Additional commit() call needed for insert/update/delete commands
			cnx.commit()
			outMsg = {'message' : 'Account successfully created. You can now log in.'}
			self.response.out.write(json.dumps(outMsg))
		#Username is already taken. Reply with error message
		else:
			outMsg = {'message' : 'An account with that email address already exists. Please try again.'}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(outMsg))			

class Logout(BaseHandler):
        def get(self):
            #clear the session upon logout
            self.session.clear()
            self.redirect("index.html")

class PassTest(webapp2.RequestHandler):
	def post(self):
		inObj = json.loads(self.request.body)
		forgottenEmail = inObj['fEmail']
		
		userQuery = ("SELECT password FROM users WHERE email = '"+forgottenEmail+"'")
		cursor.execute(userQuery)
		
		releasePass = cursor.fetchone()
		print "password is:"
		print releasePass
		if releasePass != None:
			emailMessage = text('Your password as you requested is:' + " " + releasePass[0])
			emailMessage['Subject'] = "Password Retrieval"
			emailMessage['From'] = emailUser
			emailMessage['To'] = forgottenEmail
			try:
				server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				server.ehlo()
				server.login(emailUser, emailPass)
				server.sendmail(emailUser, forgottenEmail, emailMessage.as_string())
				out_obj = {'message': 'Email was sent with password'}
				self.response.out.write(json.dumps(out_obj))
			except:
				out_obj = {'message': 'There was a problem with the server try again later'}
				self.response.out.write(json.dumps(out_obj))
		else:
			out_obj = {'message': 'Email does not exist'}
			self.response.out.write(json.dumps(out_obj))

class CreateAward(webapp2.RequestHandler):
		def post(self):
			inObj = json.loads(self.request.body)
			empEmail = inObj['empEmail']
			empName = inObj['empName']
			awardType = inObj['awdType']
			
			""" I need to be able to get the userid from sessions to get the awarding name, waiting on sessions, for now hard coding awarder name
			cursor = cnx.cursor(named_tuple=True)
			userQuery = ("SELECT password, name, email FROM users WHERE email = '"+forgottenEmail+"'")
			cursor.execute(userQuery)
			
			"""
			prelimLatex = r'''
			\documentclass[landscape]{article}
			\usepackage{wallpaper}
			\usepackage{niceframe}
			\usepackage{xcolor}
			\usepackage{ulem}
			\usepackage{graphicx}
			\usepackage{geometry}
			\geometry{tmargin=.5cm,bmargin=.5cm,
			lmargin=.5cm,rmargin=.5cm}
			\usepackage{multicol}
			\setlength{\columnseprule}{0.4pt}
			\columnwidth=0.3\textwidth

			\begin{document}

			\centering
			\scalebox{3}{\color{blue!30!black!60}
			\begin{minipage}{.33\textwidth}
			\font\border=umrandb
			\generalframe
			{\border \char113} %% up left
			{\border \char109} %% up
			{\border \char112} %% up right
			{\border \char108} %% left 
			{\border \char110} %% right
			{\border \char114} %% lower left
			{\border \char111} %% bottom
			{\border \char115} %% lower right
			{\centering



			\curlyframe[.9\columnwidth]{

			\textcolor{red!10!black!90}
			{\small Congratulations %(employee_name)s!}\\

			\textcolor{green!10!black!90}{
			\tiny %(inhonor_text)s}

			\smallskip

			\textcolor{red!30!black!90}
			{\textit{Recipient of}}

			\textcolor{black}{\large \textsc{%(award_name)s!}}

			\vspace{2mm}

			\tiny


			\vspace{20mm}


			}}
			\end{minipage}
			}
			\end{document}

			'''
			finishedLatex = prelimLatex % {'employee_name': empName, 'inhonor_text': 'Lucky Person You', 'award_name': awardType}

			outFile = open('AwardCertificate.tex', 'w')

			outFile.write(finishedLatex)

			outFile.close()

			subprocess.check_call(['pdflatex', 'AwardCertificate.tex'])

		
			msg = MIMEMultipart()
			msg['Subject'] = "You Have Recieved an Award"
			msg['From'] = "Certificate Sender" """Will be the user's name, need sessions done first"""
			msg['To'] = empEmail
			
			attachment = open('AwardCertificate.pdf', 'rb')
			
			"""Credit to http://naelshiab.com/tutorial-send-email-python/ """
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "atachment; filename=AwardCertificate.pdf")
			
			msg.attach(part)
			
			
			
			
			
			try:
				server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				server.ehlo()
				server.login(emailUser, emailPass)
				server.sendmail(emailUser, empEmail, msg.as_string())
				out_obj = {'message': 'Your Award has been sent in an email!'}
				self.response.out.write(json.dumps(out_obj))
			except:
				out_obj = {'message': 'There was a problem with the server try again later'}
				self.response.out.write(json.dumps(out_obj))
		"""else:
			out_obj = {'message': 'Email does not exist'}
			self.response.out.write(json.dumps(out_obj))"""

				
""" adapted from
http://stackoverflow.com/questions/13841827/chrome-not-rendering-stylesheets-served-by-python-webapp2
"""

class ServeCss(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/css"
		finalFileName = 'static/css/' +  self.request.get('file')
		self.response.out.write(open(finalFileName, "rb").read())

class ServeScript(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/html"
		finalFileName = 'static/script/' +  self.request.get('file')
		self.response.out.write(open(finalFileName, "rb").read())

			
			
