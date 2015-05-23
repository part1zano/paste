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
	
	with open(os.path.join(sys.path[0], 'README.md'), 'r') as f:
		content = f.read()
	
	return Markup(markdown.markdown(content))

@app.route('/<int:pasteid>') # FIXME :: syntax hl, indent is ugly
def pasteid(pasteid):
	paste = db.get_paste(pasteid)
        if request.args.get('term') == 'true':
            pass
        else:
            paste = unicode(escape(paste)).replace('	', '    ').replace(' ', '&nbsp;').replace('\n', '<br />')
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
	sys.path = ['.'] + sys.path
	app.run(debug=True, host='0.0.0.0', port=8080)
