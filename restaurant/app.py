from flask import Flask, render_template, request, session, redirect,url_for, flash
from functools import wraps
from dbUtils import r_getList, r_add, r_editList, r_update, r_delete , r_getallList,r_acceptList,r_announced_deliver#, details, add, delete, editList, update, buy, new_buy, get_shop
import os
# creates a Flask application, specify a static folder on /
#app = Flask(__name__, static_folder='static',static_url_path='/')
app = Flask(__name__, static_folder='static')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

global my_id
my_id=1
	
# 設置上傳目錄
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


#自己的拍賣品清單
@app.route("/restaurant")
#使用server side render: template 樣板
def r_get_sell():
	dat=r_getallList(my_id)
	return render_template('r_sell_list.html',data=dat, id_in=my_id)


@app.route("/r_sell_food")
#使用server side render: template 樣板
def r_get_food():
	dat=r_getList(my_id)
	return render_template('r_sell_food.html',data=dat,id_in=my_id)

@app.route("/r_new")
#使用server side render: template 樣板
def r_add_new():

	return render_template('r_add_product.html')

@app.route('/r_add_product', methods=['POST'])
def r_add_form():
    form = request.form
    name = form['name']
    price = form['price']
    detail = form['more']
    file = request.files.get('picture')

    if file and file.filename:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        picture_path=file.filename
    else:
        picture_path = "default.jpg"
    r_add(name, price, detail, picture_path, my_id)
    return redirect(url_for('r_get_food'))
	#return render_template('add_product.html')

#編輯產品submit
@app.route('/r_edit_product', methods=['POST'])
def r_edit_form():
	form = request.form
	name = form['name']
	price = form['price']
	detail = form['more']
	edit_id = form['edit_id']
	current_pix = form['current_pix']
	file = request.files.get('picture')

	if file and file.filename:
		filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(filename)
		picture_path=file.filename
	else:
		picture_path = current_pix

	r_update(name,price,detail,picture_path,edit_id)
	#dat=update(name,info,price, s_id)
	return redirect(url_for('r_get_food'))
#編輯產品頁面
@app.route("/r_edit_product/<int:id>")
#使用server side render: template 樣板
def r_edit(id):
	dat=r_editList(id)
	return render_template('r_edit_product.html', data=dat,id_in=my_id,edit_id=id)

#刪除產品
@app.route("/r_delete_product/<int:id>")
#使用server side render: template 樣板
def r_delete_form(id):
	dat=r_delete(id)
	return redirect(url_for('r_get_food'))
	#return render_template('delete.html',id)
@app.route("/r_delete_product")
#使用server side render: template 樣板
def r_delete_form_error():
	return redirect(url_for('r_get_food'))
	#return render_template('delete.html',id)

@app.route("/r_accept_ord/<int:id>")
#使用server side render: template 樣板
def r_accept(id):
	dat=r_acceptList(id)
	return redirect(url_for('r_get_sell'))

@app.route("/r_announced_deliver/<int:id>")
#使用server side render: template 樣板
def announced(id):
	dat=r_announced_deliver(id)
	return redirect(url_for('r_get_sell'))

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