import webapp2
from webapp2_extras import sessions

config = {'default-group' : 'base-data'}
config['webapp2_extras.sessions'] = {'secret_key':'cs-project-ftw',}

#Comment/uncomment hostName as needed for local/AWS testing
#hostName = 'localhost'
hostName = 'ec2-52-26-46-121.us-west-2.compute.amazonaws.com'
portNum = '5423'

app = webapp2.WSGIApplication([
(r'/', 'api.SignOnPage')
], debug=True, config=config)


def main():
	from paste import httpserver
	httpserver.serve(app, host=hostName, port=portNum)
	
app.router.add((r'/static/css.*', 'api.ServeCss'))
app.router.add((r'/static/script.*', 'api.ServeScript'))
app.router.add(webapp2.Route(r'/adapter/<id:[0-9]+><:/?>', 'api.AdapterVar'))
app.router.add(webapp2.Route(r'/productID/<pid:[0-9]+>/adapterID/<aid:[0-9]+><:/?>', 'api.Link'))
app.router.add(webapp2.Route(r'/index.html', 'api.SignOnPage'))
app.router.add(webapp2.Route(r'/about.html', 'api.AboutPage'))
app.router.add(webapp2.Route(r'/dashboard.html', 'api.DashboardPage'))
app.router.add(webapp2.Route(r'/admin.html', 'api.AdminDashboardPage'))
app.router.add(webapp2.Route(r'/users.html', 'api.UsersPage'))
app.router.add(webapp2.Route(r'/existing.html', 'api.ExistingPage'))
app.router.add(webapp2.Route(r'/signUp.html', 'api.SignUpPage'))
app.router.add(webapp2.Route(r'/createUserAccount', 'api.CreateUserAccount'))
app.router.add(webapp2.Route(r'/forget.html', 'api.ForgetPasswordPage'))
app.router.add(webapp2.Route(r'/account.html', 'api.AccountPage'))
app.router.add(webapp2.Route(r'/passTest', 'api.PassTest'))
app.router.add(webapp2.Route(r'/checkLogin', 'api.CheckLogin'))
app.router.add(webapp2.Route(r'/createAward', 'api.CreateAward'))
app.router.add(webapp2.Route(r'/logout.html', 'api.Logout'))
app.router.add(webapp2.Route(r'/accountInfo', 'api.FillAccountPage'))
app.router.add(webapp2.Route(r'/existingInfo', 'api.FillExistingPage'))

if __name__ == '__main__':
	main()
	
	
