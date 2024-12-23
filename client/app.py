from flask import Flask, render_template, request, session, redirect
from functools import wraps
from dbUtils import *
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
def c_insertdo():
	acc=request.form.get('acc')
	psw=request.form.get('psw')
	fname=request.form.get('fname')
	lname=request.form.get('lname')
	tel=request.form.get('tel')
	email=request.form.get('email')
	add=request.form.get('add')
	C_insertacc(acc, psw, fname, lname, tel, email, add)
	return render_template('c_register.html')

#客戶homepage
@app.route("/c_home")
def c_homepage():
	data=C_gethome()
	return render_template('c_homepage.html', data=data)

#條件搜尋
@app.route("/search", methods=['get','post'])
def c_search():
	option=request.form.get('select')
	data=C_gethome2(option)
	return render_template('c_homepage.html', data=data)

#已下定清單
@app.route("/c_orderlist")
def c_Olist():
	return render_template('c_orderlist.html')

#已下定清單詳細內容
@app.route("/c_orderlistinfo")
def c_Olistinfo():
	return render_template('c_orderlistinfo.html')

#收貨確認
@app.route("/c_recievecheck")
def c_check():
	return render_template('c_recievecheck.html')

#給予評價
@app.route("/c_feedbackUPL")
def c_feedback():
	return render_template('c_feedbackUPL.html')

#各餐廳菜單
@app.route("/c_Rmanu")
def c_showmanu():
	return render_template('c_Rmanu.html')

#購物車
@app.route("/c_car")
def c_showcar():
	return render_template('c_carlist.html')

#菜品詳細資訊
@app.route("/c_manuinfo")
def c_showmanuinfo():
	return render_template('c_Rmanuinfo.html')

#加入購物車
