from flask import Flask, request, redirect, url_for, render_template
import db
import re

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
	if request.method == 'POST':
		return '{0}{1}\n'.format(request.url_root, str(db.new_paste(request.form['paste'])))

	return 'this is a test pastebin' # FIXME :: add man page @ main

@app.route('/<int:pasteid>')
def pasteid(pasteid):
	paste = db.get_paste(pasteid)
	paste = re.sub('\s', '&nbsp;', paste)
	paste = re.sub('<', '&lt;', paste)
	paste = re.sub('>', '&gt;', paste)
	paste = re.sub('\n', '<br />')
	return paste


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
