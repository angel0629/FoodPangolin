from flask import Flask, render_template, request, session, redirect
from functools import wraps
from dbUtils import C_insertacc
# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID')
		if not loginID:
			return redirect('/loginPage.html')
		return f(*args, **kwargs)
	return wrapper

#客戶註冊頁面
@app.route("/") 
def c_register(): 
	return render_template('c_register.html')

#註冊內容儲存至DB
@app.route("/c_register", methods=['get','post'])
def insertdo():
	acc=request.args.get('acc')
	psw=request.args.get('psw')
	fname=request.args.get('fname')
	lname=request.args.get('lname')
	tel=request.args.get('tel')
	email=request.args.get('email')
	add=request.args.get('add')
	C_insertacc(acc, psw, fname, lname, tel, email, add)
	return render_template('c_register.html')

#客戶homepage
