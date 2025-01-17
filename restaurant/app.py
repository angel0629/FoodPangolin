from flask import Flask, render_template, request, session, redirect,url_for, flash
from functools import wraps
from dbUtils import getList, add, editList, update, delete #, getallList, details, add, delete, editList, update, buy, new_buy, get_shop

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

global my_id
my_id=1
	
#自己的拍賣品清單
@app.route("/")
#使用server side render: template 樣板
def get_sell():
	
	return render_template('sell_list.html')


@app.route("/sell_food")
#使用server side render: template 樣板
def get_food():
	dat=getList(my_id)
	return render_template('sell_food.html',data=dat,id_in=my_id)

@app.route("/new")
#使用server side render: template 樣板
def add_new():

	return render_template('add_product.html')

@app.route('/add_product', methods=['POST'])
def add_form():
	form = request.form
	name = form['name']
	price = form['price']
	more = form['more']
	picture = form['picture']
	add(name,price,more,picture,my_id)
	return redirect(url_for('get_food'))
	#return render_template('add_product.html')

#編輯產品submit
@app.route('/edit_product', methods=['POST'])
def edit_form():
	form = request.form
	name = form['name']
	price = form['price']
	more = form['more']
	picture = form['picture']
	update(name,price,more,picture,my_id)
	#dat=update(name,info,price, s_id)
	return redirect(url_for('get_food'))

#編輯產品頁面
@app.route("/edit_product/<int:id>")
#使用server side render: template 樣板
def edit(id):
	dat=editList(id)
	return render_template('edit_product.html', data=dat,id_in=my_id)

#刪除產品
@app.route("/delete_product/<int:id>")
#使用server side render: template 樣板
def delete_form(id):
	dat=delete(id)
	return redirect(url_for('get_food'))
	#return render_template('delete.html',id)

'''


#所有人的拍賣品清單頁面
@app.route("/all_sells_list")
#使用server side render: template 樣板
def get_all():
	dat=getallList()
	return render_template('all_sells_list.html', data=dat,id_in=my_id)


#新增產品submit
@app.route('/add_product', methods=['POST'])
def add_form():
	form =request.form
	name = form['name']
	info =form['info']
	price =form['price']
	add(name,info,price,my_id)
	return redirect(url_for('get_sell'))
	#return render_template('sell_list.html', data=dat)

#新增產品頁面
@app.route("/add_product")
#使用server side render: template 樣板
def add1():
	#dat=getList()
	#return render_template('add_product.html', data=dat)
	return render_template('add_product.html',id_in=my_id)


#編輯產品submit
@app.route('/edit_product', methods=['POST'])
def edit_form():
	form =request.form
	name = form['name_edit']
	info =form['info_edit']
	price =form['price_edit']
	s_id =form['s_id']
	dat=update(name,info,price, s_id)
	return redirect(url_for('get_all'))

#編輯產品頁面
@app.route("/edit_product/<int:id>")
#使用server side render: template 樣板
def edit(id):
	dat=editList(id)
	return render_template('edit_product.html', data=dat,id_in=my_id)

#刪除產品
@app.route("/delete_product/<int:id>")
#使用server side render: template 樣板
def delete_form(id):
	dat=delete(id)
	return redirect(url_for('get_sell'))
	#return render_template('delete.html',id)

#詳細資訊頁面
@app.route("/details/<int:id>")
#取得網址作為參數
def see_details(id):
	#check login inside the function
	dat=details(id)
	return render_template('details.html', data=dat,id_in=my_id)

#出價頁面
@app.route("/buy_this/<int:id>")
#取得網址作為參數
def buythis(id):
	#check login inside the function
	dat=buy(id)
	return render_template('buy_this.html', data=dat,id_in=my_id)


#出價成功
@app.route("/buy_this/<int:id>/<int:new_price>")
#取得網址作為參數
def new_buythis(id,new_price):
	#check login inside the function
	dat=new_buy(id,new_price,my_id)
	return redirect(url_for('get_shopping'))
	#return render_template('buy_this.html', data=dat)

#跳轉到購物車
@app.route("/my_shopping_list")
def get_shopping():
	dat=get_shop(my_id)
	return render_template('my_shopping_list.html',data=dat,id_in=my_id)


'''

'''
@app.route("/test/<string:name>/<int:id>")
#取得網址作為參數
def useParam(name,id):
	#check login inside the function
	if not isLogin():
		return redirect('/loginPage.html')
	return f"got name={name}, id={id} "
'''

'''
@app.route('/input', methods=['GET', 'POST'])
def userInput():
	if request.method == 'POST':
		form =request.form
	else:
		form= request.args

	txt = form['txt']  # pass the form field name as key
	note =form['note']
	select = form['sel']
	msg=f"method: {request.method} txt:{txt} note:{note} sel: {select}"
	return msg
'''

'''
@app.route('/buy_this', methods=['POST'])
def buy_form():
	form =request.form
	spend =form['spend']
	s_id =form['s_id']
	dat=buy(spend,s_id)
	return redirect(url_for('get_sell'))
'''
