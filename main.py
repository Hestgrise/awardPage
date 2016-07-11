import webapp2
import webapp2_static

config = {'default-group' : 'base-data'}

app = webapp2.WSGIApplication([
(r'/static/(.+)', webapp2_static.StaticFileHandler)
], debug=True, config=config)


def main():
	from paste import httpserver
	httpserver.serve(app, host='ec2-52-26-46-121.us-west-2.compute.amazonaws.com', port='5423')
	
app.router.add(webapp2.Route(r'/', 'api.SignOnPage'))
app.router.add(webapp2.Route(r'/adapter/<id:[0-9]+><:/?>', 'api.AdapterVar'))
app.router.add(webapp2.Route(r'/productID/<pid:[0-9]+>/adapterID/<aid:[0-9]+><:/?>', 'api.Link'))

if __name__ == '__main__':
	main()
	
	
