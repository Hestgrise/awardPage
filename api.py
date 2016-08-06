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
from copy import deepcopy

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

class RecentAwards(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		awardQuery = ("SELECT awardee, type, dateAwarded FROM awards ORDER BY dateAwarded DESC LIMIT 5")
		cursor.execute(awardQuery)
		awards = cursor.fetchall()
		names = []
		types = []
		dates = []

		for award in awards:
			names.append(str(award[0]))
			types.append(str(award[1]))
			dates.append(award[2])

		#Convert datetime objects to human readable form
		for idx in range(0, len(dates)):
			dates[idx] = dates[idx].strftime("%B %d, %Y")
		
		msg = {"names":names, "awards":types, "dates":dates}
		self.response.write(json.dumps(msg))

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

class FillUsersPage(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)

		usersQuery = ("SELECT id, name, email, dateCreated FROM users")
		cursor.execute(usersQuery)
		results = cursor.fetchall()
		ids = []
		names = []
		dates = []
		emails = []
		for result in results:
			ids.append(str(result[0]))
			names.append(str(result[1]))
			emails.append(str(result[2]))
			dates.append(result[3])
		for idx in range(0, len(dates)):
			dates[idx] = dates[idx].strftime("%B %d, %Y")

		msgBody = {"ids":ids, "names":names, "emails":emails, "dates":dates}
		self.response.out.write(json.dumps(msgBody))

		cursor.close()
		cnx.close()

class AdminsPage(BaseHandler):
	@adminLoggedIn
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('admins.html')
		self.response.out.write(template.render())

class FillAdminsPage(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)

		adminsQuery = ("SELECT id, email, dateCreated FROM admins")
		cursor.execute(adminsQuery)
		results = cursor.fetchall()
		ids = []
		dates = []
		emails = []
		for result in results:
			ids.append(str(result[0]))
			emails.append(str(result[1]))
			dates.append(result[2])
		for idx in range(0, len(dates)):
			dates[idx] = dates[idx].strftime("%B %d, %Y")

		msgBody = {"ids":ids, "emails":emails, "dates":dates}
		self.response.out.write(json.dumps(msgBody))

		cursor.close()
		cnx.close()


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

class DeleteAdminAccount(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		postData = json.loads(self.request.body)
		adminIds = postData["ids"]
		
		for adminId in adminIds:
			deleteQry = ("DELETE FROM admins WHERE id='"+adminId+"'")
			cursor.execute(deleteQry)
		cnx.commit()
		self.redirect("admins.html")

		cursor.close()
		cnx.close

class DeleteUserAccount(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)

		postData = json.loads(self.request.body)
		userIds = postData["ids"]
		
		for userId in userIds:
			deleteQry = ("DELETE FROM users WHERE id='"+userId+"'")
			cursor.execute(deleteQry)
		cnx.commit()
		self.redirect("users.html")

		cursor.close()
		cnx.close

class DeleteAwards(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)

		postData = json.loads(self.request.body)
		awardIds = postData["ids"]
		
		for awardId in awardIds:
			deleteQry = ("DELETE FROM awards WHERE id='"+awardId+"'")
			cursor.execute(deleteQry)
		cnx.commit()
		self.redirect("existing.html")

		cursor.close()
		cnx.close

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
		cursor.close()
		cnx.close()

#contacts database and returns data to the admin_dashboard page
class FilterData(BaseHandler):
        def post(self):
                cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
                cursor = cnx.cursor(buffered=True)
                postData = json.loads(self.request.body) #get the filter data
                num = int(postData['size'])
                filterQuery = "SELECT "
                userFlag = 0 # flag to denote if userId is passed in - if so, need to do a JOIN in the query
                dateFlag = -1 # flag to denote if the date was a chosen field
                #iterate to build appropriate SQL query
                for x in range(0,num):
                    key = "option"+str(x)
                    if postData[key] != "userName":
                        if postData[key] == "dateAwarded":
                            dateFlag = x #get index of the date awarded values
                        filterQuery+=("awards."+postData[key])
                    else:
                        userFlag = 1
                        filterQuery+="users.name" #name field in the users table
                    if x < num-1:
                        filterQuery+=", "
                    else:
                        filterQuery+=" "

                filterQuery+= "FROM awards"
                # add inner join if userName is passed in as a field
                if userFlag == 1:
                    filterQuery+=" INNER JOIN users ON users.id=awards.userId"

                if postData["filter"] != "none":
                    filterQuery = filterQuery + " WHERE awards." + postData["filter"] + " = '" + postData["filterVal"] + "'"

                #outMsg = {"result":filterQuery}
                #self.response.out.write(json.dumps(outMsg)) #pass back for testing
                
                cursor.execute(filterQuery) #execute the query
                results = cursor.fetchall() #fetch the results

                entry = []
                entries = []
                y=0
               # if dateFlag > -1:
               # add entries to new entries array
                for result in results:
                    entry = []
                    for y in range(0,len(result)):
                        # modify date to be a string - so it can be parsed as JSON
                        if dateFlag == y:
                            entry.append(result[y].strftime("%Y %B %d"))
                        else:     
                            entry.append(result[y])
                    entries.append(entry)

                #self.response.out.write(json.dumps(filterQuery))
                self.response.out.write(json.dumps(entries)) #send back the data in json format
                cursor.close()
                cnx.close()

#EditAccountPage shows current name and provides input field to enter new name
class EditAccountPage(BaseHandler):
	@loggedIn
	def post(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		template = env.get_template('editAccountInfo.html')
		self.response.out.write(template.render())

#Simply returns current user's name to the edit account name page
class FillEditAccountPage(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		userId = str(self.session.get('user')[0])

		nameQuery = ("SELECT name FROM users WHERE id = '"+userId+"'")
		cursor.execute(nameQuery)
		currentName = cursor.fetchone()[0].encode('utf-8')

		msg = {'currentName': currentName}
		self.response.write(json.dumps(msg))

		cursor.close()
		cnx.close()

#Applies user edits to name (updates name field in database)
class EditAccount(BaseHandler):
	def post(self):
		cnx = mysql.connector.connect(user=dbUser, password=dbPass, host=dbHost, database=dbName)
		cursor = cnx.cursor(buffered=True)
		userId = str(self.session.get('user')[0])
		newName = self.request.get('newName')
		updateQuery = ("UPDATE users SET name = '"+newName+"' WHERE id = '"+userId+"'")
		cursor.execute(updateQuery)
		cnx.commit()
		cursor.close()
		cnx.close()
		self.redirect('/account.html')


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
		# queries will either query admins or users table, depending on the login typ
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
			dateAwarded = inObj['dateAwarded']
			
			print str(dateAwarded);

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
			{\textit{Is Recognizing You For}}

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

			#First we get our user Signature
			userQuery = ("SELECT signature FROM users WHERE id = '"+userID+"'")
			cursor.execute(userQuery)
		
			userSig = cursor.fetchone()[0]
			
			#Now we get the name of our user making the award
			userQuery = ("SELECT name FROM users WHERE id = '"+userID+"'")
			cursor.execute(userQuery)
		
			userName = cursor.fetchone()[0]
			
			#Now we take our date time and split it to parse it for the certificate
			#Make a copy of date time string
			dateAwardedCopy = dateAwarded
			dateTimeList = dateAwardedCopy.split("-")
			#print "date time list 1: ", dateTimeList[0], " datetimelist list 2 is: ", dateTimeList[1], " datetimelist 3 is: ", dateTimeList[2]

			#This is our year to print on the certificate
			certYear = dateTimeList[0]
			
			#We get our month to print out
			if dateTimeList[1] == '01':
				certMonth = 'January'
			elif dateTimeList[1] == '02':
				certMonth = 'February'
			elif dateTimeList[1] == '03':
				certMonth = 'March'
			elif dateTimeList[1] == '04':
				certMonth = 'April'
			elif dateTimeList[1] == '05':
				certMonth = 'May'
			elif dateTimeList[1] == '06':
				certMonth = 'June'
			elif dateTimeList[1] == '07':
				certMonth = 'July'
			elif dateTimeList[1] == '08':
				certMonth = 'August'
			elif dateTimeList[1] == '09':
				certMonth = 'September'
			elif dateTimeList[1] == '10':
				certMonth = 'October'				
			elif dateTimeList[1] == '11':
				certMonth = 'November'				
			elif dateTimeList[1] == '12':
				certMonth = 'December'				
			
			#Now we pull out the day as well to separate it from the time
			dayTimeList = dateTimeList[2].split('T')
			
			if dayTimeList[0] == '01':
				certDay = '1st'
			elif dayTimeList[0] == '02':
				certDay = '2nd'
			elif dayTimeList[0] == '03':
				certDay = '3rd'
			elif dayTimeList[0] == '21':
				certDay = '21st'
			elif dayTimeList[0] == '22':
				certDay = '22nd'
			elif dayTimeList[0] == '23':
				certDay = '23rd'
			elif dayTimeList[0] == '31':
				certDay = '31st'
			else:
				certDay = (str(int(dayTimeList[0])) + 'th')
				
			finalNameAndDate = userName + " this " + certDay + " day of " + certMonth + ", " + certYear
				
			#print "CertYear: ", certYear, " certMonth ", certMonth, " certDay ", certDay
	
			#This gets our variables into the latex template above
			finishedLatex = prelimLatex % {'employee_name': empName, 'inhonor_text': finalNameAndDate, 'award_name': awardType, 'signature_image': str(userSig)}

			#Mow we write our .tex file
			outFile = open('AwardCertificate.tex', 'w')

			outFile.write(finishedLatex)

			outFile.close()

			#This calls pdflatex on the command line to output the certificate
			subprocess.check_call(['pdflatex', 'AwardCertificate.tex'])

			#the Next lines set up the email to send the Certificate
			msg = MIMEMultipart()
			msg['Subject'] = "You Have Recieved an Award"
			msg['From'] = userName
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
			#instant = datetime.datetime.now()
			userDetails = (userID, awardType, empName, empEmail, str(dateAwarded))
			userInsert = ("INSERT INTO awards (userId, type, awardee, email, dateAwarded) VALUES (%s, %s, %s, %s, %s)")
			cursor.execute(userInsert, userDetails)
			#Additional commit() call needed for insert/update/delete commands
			cnx.commit()

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

			
			
