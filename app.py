from flask import Flask, render_template, request, flash, jsonify
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
		for num in SO_ID:
			if num.isalpha():
				flash("Please submit a valid ID. No letters.")
				found_error = True
				break
		if len(SO_ID) != 7:
			flash("Invalid length. Try again.")
			found_error = True
		if found_error:
			return render_template('index.html')
		else:		
			posts = SO.fetch('/users/{ids}/posts', ids=[SO_ID], pagesize=5)
			try:
				name = posts["items"][0]["owner"]["display_name"]
				profile_pic = posts["items"][0]["owner"]["profile_image"]
				links = []
				for item in posts["items"]:
					links.append(item['link'])
				scores = []
				for item in posts["items"]:
					scores.append(item['score'])
				post_data = []
				for item in posts["items"]:
					post_data.append([item["post_id"], item["post_type"]])
				parser = htmlparser.HTMLParser()
				for p in post_data:
					if p[1] == "answer":
						title = SO.fetch('/answers/{ids}/questions', ids=[p[0]])["items"][0]["title"]
						u_title = parser.unescape(title)
						p.append(u_title)
					else:
						title = SO.fetch('/questions/{ids}', ids=[p[0]])["items"][0]["title"]
						u_title = parser.unescape(title)
						p.append(u_title)
				all_data = list(zip(post_data, links, scores))
				for data in all_data:
					data[0].extend([data[1]])
					data[0].extend([data[2]])
					#del data[1]
				raw_data = [a[0] for a in all_data]
				#return jsonify(raw_data)
				return render_template('results.html', username=name, pfp=profile_pic, posts=raw_data)
			except Exception as e:
				flash(e)
				return render_template('index.html')
	return render_template('index.html')

@app.route('/results')
def results():
	return render_template('results.html', username="Mangohero1")

if __name__ == "__main__":
	app.run(debug=True)