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

#客戶homepage #無任何商品菜單之餐廳不會顯示於列表上
@app.route("/c_home")
def c_homepage():
	data=C_gethome()
	return render_template('c_homepage.html', data=data)

#條件搜尋(下拉)
@app.route("/search", methods=['get','post'])
def c_search():
	option=request.form.get('select')
	text=request.form.get('text')
	data=C_gethome2(option, text)
	return render_template('c_homepage.html', data=data)

#各餐廳菜單
@app.route("/c_Rmenu/<string:Rname>/<int:Rid>")
def c_showmanu(Rname, Rid):
	data=C_getmenu(Rid)
	fbdata=C_getfeedback(Rid)
	return render_template('c_Rmanu.html', data=data, Rname=Rname, Rid=Rid, fbdata=fbdata)

#菜品詳細資訊
@app.route("/c_menuinfo/<string:Rname>/<int:Rid>/<string:Mname>/<int:Mid>")
def c_showmanuinfo(Rname, Rid, Mname, Mid):
	data=C_getmenuinfo(Rid, Mid)
	return render_template('c_Rmanuinfo.html',data=data, Rname=Rname, Rid=Rid, Mname=Mname, Mid=Mid)

#加入購物車
@app.route("/c_addcar/<string:Rname>/<int:Rid>/<string:Dname>/<int:Dprice>/<int:Num>/<int:Sum>")
def c_addtocar(Rname, Rid, Dname, Dprice, Num, Sum):
	data=C_getmenu(Rid)
	fbdata=C_getfeedback(Rid)
	C_addcar(Rname, Dname, Dprice, Num, Sum)
	return render_template('c_Rmanu.html', data=data, Rname=Rname, Rid=Rid, fbdata=fbdata)

#購物車
@app.route("/c_car/<string:Rname>/<int:Rid>")
def c_showcar(Rname, Rid):
	data=C_getcar(Rname)
	total=C_getcartotal(Rname)['total']
	return render_template('c_carlist.html', data=data, Rname=Rname, total=total, Rid=Rid)

#購物車：移除
@app.route("/c_delcar/<string:Rname>/<int:Rid>/<string:Dname>")
def c_rmcar(Rname, Rid, Dname):
	C_removecar(Rname, Dname)
	data=C_getcar(Rname)
	total=C_getcartotal(Rname)['total']
	return render_template('c_carlist.html', data=data, Rname=Rname, total=total, Rid=Rid)

#下單
@app.route("/c_addorder/<string:Rname>")
def c_addorder(Rname):
	C_addorder(Rname)
	data=C_gethome()
	return render_template('c_homepage.html', data=data)

#已下定清單
@app.route("/c_orderlist")
def c_Olist():
	data=C_getorderlist()
	return render_template('c_orderlist.html', data=data)

#已下定清單詳細內容
@app.route("/c_orderlistinfo/<string:Rname>")
def c_Olistinfo(Rname):
	data=C_getorderinfo(Rname)
	statusid=data[0]['status']
	status=C_getstatus(statusid)['status']
	sum=data[0]['sum']
	data_Dname=data[0]['Dname'].split(",")
	data_Dprice=data[0]['Dprice'].split(",")
	data_Num=data[0]['num'].split(",")
	data2=[]
	for i in range(len(data_Dname)):
		data2.append({
        'Dname': data_Dname[i].strip(),
        'Dprice': int(data_Dprice[i].strip()),
        'num': int(data_Num[i].strip())
    })
	return render_template('c_orderlistinfo.html', Rname=Rname, sum=sum, status=status, data2=data2)

#收貨確認
@app.route("/c_recievecheck")
def c_check():
	return render_template('c_recievecheck.html')

#給予評價
@app.route("/c_feedbackUPL")
def c_feedback():
	return render_template('c_feedbackUPL.html')

