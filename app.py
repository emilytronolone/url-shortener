#pipenv install
#pipenv shell
#pipenv install flask
#export FLASK_APP=name (automatically detects app.py)
#development env: export FLASK_ENV=development
#flask run

#Flask => to create Flask app
#render_template => render html files for use
#request => retrieve input data
#redirect => to url (oarameter is a path)
#url_for => parameter is function
#flask => flashes alerts
# abort => error messaging
#session => allows us to access cookies
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import json
import os.path
#checks if file is safe to save
#werkzeug is from Flask
from werkzeug.utils import secure_filename

#create Flask app
app = Flask(__name__)
#allows to securely send messages back and forth from user
#provide random string for key
app.secret_key = 'uierhbf734y'

#create first route
#string is path name
@app.route('/')
#route function uses html file
def home():
	#use cookies as parameter
	return render_template('home.html', codes=session.keys())

#new route that displays '/your-url' in url
#accepts get and post request methods
@app.route('/your-url', methods=['GET', 'POST'])
#route function
def your_url():
	#only works for post method
	#post method will not display extra data in url
	if request.method == 'POST':
		#dict of codes and urls
		urls = {}
		#checks if json file already exists (to avoid overwrite)
		if os.path.exists('urls.json'):
			with open('urls.json') as urls_file:
				#load file into dict
				urls = json.load(urls_file)

		#if code has already been used
		if request.form['code'] in urls.keys():
			flash('That short name has already been taken. Please select another name.')
			return redirect(url_for('home'))

		#checks if url or file
		if 'url' in request.form.keys():
			urls[request.form['code']] = {'url':request.form['url']}
		else:
			f = request.files['file']
			#prevents duplicate file names
			full_name = request.form['code'] + secure_filename(f.filename)
			#save file with name as full_name in directory
			f.save('/Users/emily/Desktop/url-shortener/static/user_files/' + full_name)
			#update urls.json
			urls[request.form['code']] = {'file':full_name}

		#write codes and urls to json file
		with open('urls.json','w') as url_file:
			json.dump(urls, url_file)
			#save code into cookie
			session[request.form['code']] = True
		#loads your-url page
		return render_template('your_url.html', code=request.form['code'])
	else:
		#redirects to home function
		return redirect(url_for('home'))

#url functionality
#url with string => save as code variable
@app.route('/<string:code>')
def redirect_to_url(code):
	#check if dictionary exists (urls.json)
	if os.path.exists('urls.json'):
		with open('urls.json') as urls_file:
			urls = json.load(urls_file)
			#search for code in keys
			if code in urls.keys():
				#url
				if 'url' in urls[code].keys():
					return redirect(urls[code]['url'])
				#file upload
				else:
					return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
	#return 404 error message if code does not exist
	return abort(404)

#custom 404 error page
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
