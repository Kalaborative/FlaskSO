from flask import Flask, render_template, request, flash, jsonify, redirect, url_for, session
from stackapi import StackAPI
from sys import exit
from os import urandom
import html.parser as htmlparser


SO = StackAPI('stackoverflow', key="FBFOiPEa89XOPM2tK0Zhbg((")

app = Flask(__name__)
app.secret_key = urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		SO_ID = request.form["inputID"]
		found_error = False
		found_error = not all([num.isdigit() for num in SO_ID])
		if found_error:
			flash("Please submit a valid ID. Numbers only!")
		if len(SO_ID) != 7:
			flash("Invalid length. Try again.")
			found_error = True
		if found_error:
			return render_template('index.html')
		else:		
			posts = SO.fetch('/users/{ids}/posts', ids=[SO_ID], pagesize=5)
			try:
				session['name'] = posts["items"][0]["owner"]["display_name"]
				session['profile_pic'] = posts["items"][0]["owner"]["profile_image"]
				session['raw_data'] = generate_data(posts)
				return redirect(url_for('results', uuid=SO_ID, user=session.get('name')))
			except Exception as e:
				flash(e)
				return render_template('index.html')
	return render_template('index.html')

def generate_data(json):
	links = []
	for item in json['items']:
		links.append(item['link'])
	scores = []
	for item in json["items"]:
		scores.append(item['score'])
	post_data = []
	for item in json["items"]:
		post_data.append([item["post_id"], item["post_type"]])
	parser = htmlparser.HTMLParser()
	for p in post_data:
		if p[1] == "answer":
			title = SO.fetch('/answers/{ids}/questions', ids=[p[0]])["items"][0]["title"]
		else:
			title = SO.fetch('/questions/{ids}', ids=[p[0]])["items"][0]["title"]
		p.append(parser.unescape(title))
	all_data = list(zip(post_data, links, scores))
	for data in all_data:
		data[0].extend([data[1]])
		data[0].extend([data[2]])
	raw_data = [a[0] for a in all_data]
	return raw_data

@app.route('/results/<uuid>/<user>')
def results(uuid, user):
	name = session.get('name')
	if name == user:
		profile_pic = session.get('profile_pic')
		raw_data = session.get('raw_data')
		return render_template('results.html', username=name, pfp=profile_pic, posts=raw_data)
	else:
		return render_template('results.html', username=user, pfp=None, posts=None)

if __name__ == "__main__":
	app.run(debug=True)