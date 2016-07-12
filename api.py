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

dbName = 'lambda'
dbUser = 'student'
dbPass = 'default'
dbHost = 'localhost'

#Create database connection and cursor for queries
cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='ESDR2')
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
		if passwordInDB == password:
			#Redirect to landing page
		else:
			#Error message. Try again

class CreateUserAccount(webapp2.RequestHandler):
	def post(self):
		username = self.request.get('username')
		name = self.request.get('name')
		password = self.request.get('password')
		signature = "haven't figured this out yet"
		instant = "use datetime.datetime.now()"

		userDetails = (name, username, password, instant, signature)
		userInsert = ("INSERT INTO users (name, email, password, dateCreated, signature) VALUES (%s, %s, %s, %s, %s)")
		#Additional execute() call needed for insert/update/delete commands
		cursor.execute(userInsert, userDetails)



			
			
