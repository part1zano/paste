from flask import Flask, request, redirect, url_for, render_template, escape, Markup
import db
import markdown
import sys
import os
import random

numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
actions = ['plus', 'minus', 'multiplied by']

def perform_math(arg1, arg2, action):
	if action == 'plus':
		return numbers.index(arg1)+ numbers.index(arg2)
	elif action == 'minus':
		return numbers.index(arg1) - numbers.index(arg2)
	else:
		return numbers.index(arg1) * numbers.index(arg2)


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
		arg1 = request.form['arg1']
		arg2 = request.form['arg2']
		action = request.form['action']
		if perform_math(arg1, arg2, action) == int(request.form['result']):
			return redirect('{0}{1}'.format(request.url_root, db.new_paste(request.form['paste'])))
		return 'wrong captcha'
	return '''
<form method="POST" action="/new">
	<textarea name="paste" cols="80" rows="25"></textarea><br />
	{arg1} {action} {arg2} = <input type="text" name="result" />
	<input type="hidden" name="arg1" value="{arg1}" />
	<input type="hidden" name="arg2" value="{arg2}" />
	<input type="hidden" name="action" value="{action}" />
	<input type="submit" value="Paste" />
</form>'''.format(arg1=numbers[random.randint(0, len(numbers)-1)], arg2=numbers[random.randint(0, len(numbers)-1)], action=actions[random.randint(0, len(actions)-1)])

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
