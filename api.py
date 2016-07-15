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
import smtplib
from email.mime.text import MIMEText as text

dbName = 'lambda'
dbUser = 'student'
dbPass = 'default!'
dbHost = 'localhost'

emailUser = 'certifcatecenter@gmail.com'
emailPass = 'CapStone16'

#Create database connection and cursor for queries
cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
cursor = cnx.cursor(buffered=True)

class SignOnPage(webapp2.RequestHandler):
	def get(self):
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

class DashboardPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('dashboard.html')
		self.response.out.write(template.render())

class UsersPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('users.html')
		self.response.out.write(template.render())

class ExistingPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('existing.html')
		self.response.out.write(template.render())

class SignUpPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('signUp.html')
		self.response.out.write(template.render())

class AccountPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('account.html')
		self.response.out.write(template.render())

class ForgetPasswordPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('forget.html')
		self.response.out.write(template.render())

class CheckLogin(webapp2.RequestHandler):
	def post(self):
		#Simple example of login validation to show mysql connector syntax
		validLogin = False
		#Assume the sign on page POSTS a username and password
		username = self.request.get('username', default_value=None)
		password = self.request.get('password', default_value=None)
		#(1)Create the MySQL command, (2)Execute it
		userQuery = ("SELECT password FROM users WHERE name = '"+username+"'")
		cursor.execute(userQuery)
		passwordInDB = cursor.fetchone()
		#Check entered password against user's stored password
		"""if passwordInDB == password:
			#Redirect to landing page
		else:
			#Error message. Try again"""

class CreateUserAccount(webapp2.RequestHandler):
	def post(self):
		username = self.request.get('email')
		fName = self.request.get('firstName')
		lName = self.request.get('lastName')
		name = fName + " " + lName
		password = self.request.get('password')
		signature = "haven't figured this out yet"
		instant = datetime.datetime.now()
		print("email is " + username)
		
		userDetails = (name, username, password, instant, signature)
		userInsert = ("INSERT INTO users (name, email, password, dateCreated, signature) VALUES (%s, %s, %s, %s, %s)")
		cursor.execute(userInsert, userDetails)
		#Additional commit() call needed for insert/update/delete commands
		cnx.commit()
		return self.redirect("/dashboard.html")

class PassTest(webapp2.RequestHandler):
	def post(self):
		forgottenEmail = self.request.get('fEmail')
		cursor = cnx.cursor(named_tuple=True)
		userQuery = ("SELECT password, name, email FROM users WHERE email = '"+forgottenEmail+"'")
		cursor.execute(userQuery)
		
		releasePass = cursor.fetchone()
		
		if releasePass != None:
			emailMessage = text('Your password as you requested is:' + " " + releasePass.password)
			emailMessage['Subject'] = "Password Retrieval"
			emailMessage['From'] = emailUser
			emailMessage['To'] = forgottenEmail
			try:
				server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				server.ehlo()
				server.login(emailUser, emailPass)
				server.sendmail(emailUser, forgottenEmail, emailMessage.as_string())
				print "email sent!"
			except:
				print "Something went wrong"
		else:
			print "Email doesn't exist"
		"""print(forgottenEmail)"""
		
		
		
""" adapted from
http://stackoverflow.com/questions/13841827/chrome-not-rendering-stylesheets-served-by-python-webapp2
"""

class ServeCss(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/css"
		finalFileName = 'static/css/' +  self.request.get('file')
		self.response.out.write(open(finalFileName, "rb").read())

		

			
			
