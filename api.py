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
import io
import imghdr
import uuid

import subprocess
from webapp2_extras import sessions

dbName = 'lambda'
dbUser = 'student'
dbPass = 'default'
dbHost = 'localhost'

emailUser = 'certifcatecenter@gmail.com'
emailPass = 'CapStone16'

#Create database connection and cursor for queries


#loggedIn will check to see if the user is logged in yet
#being loggedIn depends on whether the browser has user as a session variable
def loggedIn(handler):
    def checkLogin(self):
        # if the user is logged in, then return the appropriate handler
        if 'user' in self.session:
            return handler(self)
        # if the user is not logged in, then redirect to the sign in page
        elif 'admin' in self.session:
            self.redirect("admin_dashboard.html")
        # if not logged in, redirect to home page
        else:
            self.redirect("index.html")

    return checkLogin

# checks if an admin is logged in - if not, redirects appropriately
def adminLoggedIn(handler):
    def checkAdminLogin(self):
        # if admin is logged in, then return the appropriate handler
        if 'admin' in self.session:
            return handler(self)
        # if a user is logged in, then redirect to dashboard
        elif 'user' in self.session:
            self.redirect("dashboard.html")
        # if not logged in, redirect to the home page
        else:
            self.redirect("index.html")

    return checkAdminLogin


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

class AboutPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('about.html')
		self.response.out.write(template.render())

#dashboard for regular users
class DashboardPage(BaseHandler):
        @loggedIn
        def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('dashboard.html')
		self.response.out.write(template.render())

#dashboard for admin
class AdminDashboardPage(BaseHandler):
        @adminLoggedIn
        def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('admin_dashboard.html')
		self.response.out.write(template.render())

#class for users page - admin page
class UsersPage(BaseHandler):
        @adminLoggedIn
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

class FillExistingPage(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		userId = str(self.session.get('user')[0])
		#Get all awards created by current user
		userAwardsQuery = ("SELECT id, type, awardee, dateAwarded FROM awards WHERE userId = '"+userId+"'")
		cursor.execute(userAwardsQuery)
		results = cursor.fetchall()

		#Populate arrays with each value to use to fill table in HTML
		ids = []
		types = []
		winners = []
		dates = []
		for result in results:
			ids.append(str(result[0]))
			types.append(str(result[1]))
			winners.append(str(result[2]))
			dates.append(result[3])

		#Convert datetime object to human readable form
		for idx in range(0, len(dates)):
			dates[idx] = dates[idx].strftime("%B %d, %Y")

		msgBody = {"ids":ids, "types":types, "winners":winners, "dates":dates}
		self.response.out.write(json.dumps(msgBody))

		cursor.close()
		cnx.close()


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

class FillAccountPage(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		userId = str(self.session.get('user')[0])

		userInfoQuery = ("SELECT name, email, dateCreated FROM users WHERE id = '"+userId+"'")
		cursor.execute(userInfoQuery)
		userInfo = cursor.fetchone()

		name = userInfo[0].encode('utf-8')
		email = userInfo[1].encode('utf-8')
		date = userInfo[2]
		prettyDate = date.strftime("%B %d, %Y")

		numAwardsQuery = ("SELECT count(*) FROM awards WHERE userId = '"+userId+"'")
		cursor.execute(numAwardsQuery)
		numAwards = cursor.fetchone()
		numAwards = str(numAwards[0])

		msgBody = {"accountName" : name, "accountEmail" : email, "accountDate" : prettyDate, "accountAwards" : numAwards}
		self.response.out.write(json.dumps(msgBody))
		print "Cursor closed"
		cursor.close()
		cnx.close()

class ForgetPasswordPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('forget.html')
		self.response.out.write(template.render())

class CheckLogin(BaseHandler):
	def post(self):
		#Login page POSTS a username and password
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		postData = json.loads(self.request.body)
		accountType = postData['accountType'] #get the account type to differentiate between admin and regular login
		username = postData['email']
		password = postData['password']
		#hashedPass = hashlib.sha1(password).hexdigest();
		#(1)Create the MySQL command, (2)Execute it
		# queries will either query admins or users table, depending on the login type
                if accountType == "admin":
			userQuery = ("SELECT password FROM admins WHERE email = '"+username+"'")
                else:
			userQuery = ("SELECT password FROM users WHERE email = '"+username+"'")
		cursor.execute(userQuery)
		passwordQuery = cursor.fetchone()
		#Check entered password against user's stored password
		if passwordQuery != None:
			passwordInDb = passwordQuery[0].encode('utf-8')
			if passwordInDb == password:
				#get user ID from the database to add to sessions
				idQuery = ("SELECT id FROM users WHERE email = '"+username+"'")
				cursor.execute(idQuery)
				idValue = cursor.fetchone()

				# differentiate between successful user and admin login
				# send different response messages
                                # also set sessions differently based on admin or user
                                if accountType == "admin":
                                        self.session['admin'] = idValue
                                        outMsg = {'message' : 'Admin Login successful'}
                                else:
                                        self.session['user'] = idValue
					outMsg = {'message' : 'Login successful.'}
				self.response.out.write(json.dumps(outMsg))
			else:
				outMsg = {"message" : "That password doesn't match our records. Please try again."}
				self.response.out.write(json.dumps(outMsg))
		else:
			outMsg = {'message' : "There is no account associated with that email address."}
			self.response.out.write(json.dumps(outMsg))
		cursor.close()
		cnx.close()
		print "Connection closed"

class CreateUserAccount(webapp2.RequestHandler):
	def post(self):		
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		signature =  self.request.get("signatureFile")
		username = self.request.get("email")
		fName = self.request.POST.get("firstName")
		lName = self.request.POST.get("lastName")
		name = fName + " " + lName
		password = self.request.get("password")
		instant = datetime.datetime.now()
	
		usernameTakenTest = ("SELECT * FROM users WHERE email = '"+username+"'")
		cursor.execute(usernameTakenTest)

		testResult = cursor.fetchone()
		#Username is available
		if testResult == None:
			cwd = os.getcwd()
			uniqueName = uuid.uuid4()
			filename =  cwd + "/images/" + str(uniqueName)
			with open(filename, 'wb') as imgFile:
				imgFile.write(signature)
			userDetails = (name, username, password, instant, str(uniqueName))
			userInsert = ("INSERT INTO users (name, email, password, dateCreated, signature) VALUES (%s, %s, %s, %s, %s)")
			cursor.execute(userInsert, userDetails)
			#Additional commit() call needed for insert/update/delete commands
			cnx.commit()
			outMsg = {'message' : 'Account successfully created. You can now log in.'}

			#This resaves the signature file with the correct file extension
			fullName = filename + '.' + imghdr.what(filename) 

			os.rename(filename, fullName)

			self.response.out.write(json.dumps(outMsg))
		#Username is already taken. Reply with error message
		else:
			outMsg = {'message' : 'An account with that email address already exists. Please try again.'}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(outMsg))			
		cursor.close()
		cnx.close()
		print "Connection closed"
		
class Logout(BaseHandler):
        def get(self):
            #clear the session upon logout
            self.session.clear()
            self.redirect("index.html")

class PassTest(webapp2.RequestHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
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
		cursor.close()
		cnx.close()
		print "Connection closed"
		
class CreateAward(BaseHandler):
		def post(self):
			cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
			cursor = cnx.cursor(buffered=True)
			inObj = json.loads(self.request.body)
			empEmail = inObj['empEmail']
			empName = inObj['empName']
			awardType = int(inObj['awdType'])
		        if awardType == 1:
                            awardType = "Employee of the Month!"
                        elif awardType == 2:
                            awardType = "Employee of the Year!"
                        elif awardType == 3:
                            awardType = "Peer Recognition!"
                        elif awardType == 4:
                            awardType = "Excellence in Achievement!"

			""" I need to be able to get the userid from sessions to get the awarding name, waiting on sessions, for now hard coding awarder name
			cursor = cnx.cursor(named_tuple=True)
			userQuery = ("SELECT password, name, email FROM users WHERE email = '"+forgottenEmail+"'")
			cursor.execute(userQuery)
			
			"""
			prelimLatex = r'''
			\documentclass[landscape]{article}
			\usepackage{wallpaper}
			\usepackage{graphicx}
			\graphicspath{ {images/} }
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

			\tiny

			\vspace{3mm}
			\includegraphics[width=4cm,height=2cm,keepaspectratio]{%(signature_image)s}

			}}
			\end{minipage}
			}
			\end{document}

			'''
			
			#Now we have to get our user's signature file name for the latex certificate as well as write the award information			
			userID = str(self.session['user'][0])

			
			userQuery = ("SELECT signature FROM users WHERE id = '"+userID+"'")
			cursor.execute(userQuery)
		
			userSig = cursor.fetchone()[0]
		
                        #This gets our variables into the latex template above
			finishedLatex = prelimLatex % {'employee_name': empName, 'inhonor_text': 'Lucky Person You', 'award_name': awardType, 'signature_image': str(userSig)}

                        #Mow we write our .tex file
			outFile = open('AwardCertificate.tex', 'w')

			outFile.write(finishedLatex)

			outFile.close()

                        #This calls pdflatex on the command line to output the certificate
			subprocess.check_call(['pdflatex', 'AwardCertificate.tex'])

		        #the Next lines set up the email to send the Certificate
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
			
			
			
			
			#This sends the generated email with our attachment
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



                        #Now we write our Award to the database
                        
                        #userDetails = (name, username, password, instant, str(uniqueName))
			#userInsert = ("INSERT INTO users (name, email, password, dateCreated, signature) VALUES (%s, %s, %s, %s, %s)")
			#cursor.execute(userInsert, userDetails)
			#Additional commit() call needed for insert/update/delete commands
			#cnx.commit()

                        cursor.close()
			cnx.close()



				
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

			
			
