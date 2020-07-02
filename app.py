#Flask => to create Flask app
#render_template => render html files for use
#request = retrieve input data
from flask import Flask, render_template, request

#create Flask app
app = Flask(__name__)

#create first route
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
		return render_template('your_url.html', code=request.form['code'])
	else:
		return 'This is not valid.'