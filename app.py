from flask import Flask, request, redirect, url_for, render_template
import db
import re

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
	if request.method == 'POST':
		return url_for('/{0}'.format(db.new_paste(request.form['paste'])))

	return 'this is a test pastebin'

@app.route('/<int:pasteid>')
def pasteid(pasteid):
	return re.sub('\n', '<br />', db.get_paste(pasteid))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
