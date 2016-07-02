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

import json


class SignOnPage(webapp2.RequestHandler):
	def get(self):
		env = Environment(loader=PackageLoader('api', '/templates'))
		
		template = env.get_template('signon.html')
		self.response.out.write(template.render())

	def post(self):
		out_obj = {}

		out_obj = {'msg': 'Success, Your POST worked!'}
		self.response.out.write(json.dumps(out_obj))
			
			
