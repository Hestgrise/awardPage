import webapp2
import webapp2_static

config = {'default-group' : 'base-data'}

#Comment/uncomment hostName as needed for local/AWS testing
hostName = 'localhost'
#hostName = 'ec2-52-26-46-121.us-west-2.compute.amazonaws.com'
portNum = '5432'

app = webapp2.WSGIApplication([
(r'/static/(.+)', webapp2_static.StaticFileHandler)
], config = {'webapp2_static.static_file_path': './static'})


def main():
	from paste import httpserver
	httpserver.serve(app, host=hostName, port=portNum)
	
app.router.add(webapp2.Route(r'/', 'api.SignOnPage'))
app.router.add(webapp2.Route(r'/adapter/<id:[0-9]+><:/?>', 'api.AdapterVar'))
app.router.add(webapp2.Route(r'/productID/<pid:[0-9]+>/adapterID/<aid:[0-9]+><:/?>', 'api.Link'))

if __name__ == '__main__':
	main()
	
	
