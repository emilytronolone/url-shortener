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
from flask import Flask, render_template, request, redirect, url_for
import json
import os.path

#create Flask app
app = Flask(__name__)

#create first route
#string is path name
@app.route('/')
#route function uses html file
def home():
	return render_template('home.html')

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
			return redirect(url_for('home'))

		urls[request.form['code']] = {'url':request.form['url']}
		#write codes and urls to json file
		with open('urls.json','w') as url_file:
			json.dump(urls, url_file)
		#loads your-url page
		return render_template('your_url.html', code=request.form['code'])
	else:
		#redirects to home function
		return redirect(url_for('home'))