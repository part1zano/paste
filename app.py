from flask import Flask, request, redirect, url_for, render_template, escape, Markup
import db
import markdown
import sys
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
	if request.method == 'POST':
		return '{0}{1}\n'.format(request.url_root, db.new_paste(request.form['paste']))
	
	content = db.get_paste(1) # the main page must be stated as paste (id(1))

	return Markup(markdown.markdown(content))

@app.route('/<int:pasteid>') # FIXME :: syntax hl, indent is ugly
def pasteid(pasteid):
	paste = db.get_paste(pasteid)
	if request.args.get('term') in ('true', 'yes'):
		pass
	else:
		paste = u'<pre>{0}</pre>'.format(paste)
	return paste

@app.route('/new', methods=['POST', 'GET']) # FIXME :: template for form, bootstrap form
def form():
	if request.method == 'POST':
		return redirect('{0}{1}'.format(request.url_root, db.new_paste(request.form['paste'])))
	return '''
<form method="POST" action="/new">
	<textarea name="paste" cols="80" rows="25"></textarea><br />
	<input type="submit" value="Paste" />
</form>'''

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
