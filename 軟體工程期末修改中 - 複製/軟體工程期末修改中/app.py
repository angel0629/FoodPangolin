from flask import Flask , render_template ,request , session , redirect,url_for
from functools import wraps
import os
from Database import *
#app = Flask(__name__ , static_folder = 'static' , static_url_path = '/')
app = Flask(__name__ , static_folder = 'static/img')
app.config['SECRET_KEY'] = '123456/-+*'

products=[]
#global my_id

def login_confirm_acc_and_pwd(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        login_acc = session.get('loginAcc')
        if not login_acc:
            return redirect('/login_or_register.html')
        return f(*args,**kwargs)
    return wrapper

@app.route('/')
def to_login_or_register():
     return redirect('/login_or_register')

@app.route('/login_or_register', methods=['POST', 'GET'])
def loginforall():
    if request.method == 'POST':
        form = request.form
        account = form['Account']
        password = form['Password']
        identity = form['identity']  # 獲取選擇的身分

        # 從資料庫中獲取用戶資料
        user = get_users_from_db(account, password, identity)
        
        if user:  # 如果有找到對應的用戶資料
            session['loginAcc'] = account
            session['identity'] = identity  # 儲存選擇的身分
            
            # 根據身份跳轉到不同的主頁
            if identity == '消費客戶':
                return redirect("/c_home")  # 跳轉到消費者主頁
            elif identity == '餐廳業者':
                return redirect('/restaurant_sell_list')  # 跳轉到餐廳業者主頁
            elif identity == '外送人員':
                return redirect('/delivery_home')  # 跳轉到外送員主頁
            else:
                return redirect('/home')  # 預設主頁（如果身份不正確）
        else:
            error = '帳號或密碼輸入錯誤'
            return render_template('login_or_register.html', error=error)  # 傳遞錯誤訊息

    # 如果是 GET 請求，顯示登錄頁面
    return render_template('login_or_register.html')

#登出
@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect('login_or_register')

# @app.route('/customer_home')
# def home1():
    # if 'loginAcc' not in session:
    #     return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    
    # account = session['loginAcc']
    # cart_data = get_customer_cart_from_sql(account, cart_id=1)
    # if not cart_data:  # 如果 cart_data 是 None 或空
    #     cart_data = "目前沒有購物車資料"  # 可以顯示一個提示訊息

    # return render_template('user_home2.html', data=cart_data)


# 客戶homepage 無任何商品菜單之餐廳不會顯示於列表上
@app.route('/c_home')
def c_homepage():
    if 'loginAcc' not in session:
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    
    account = session['loginAcc']
    my_id_dict= get_customer_cart_from_sql(account)
    global my_id
    my_id=my_id_dict["ca_Id"]
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入
    data=C_gethome()
	
    return render_template('c_homepage.html', data=data)
    
    #bestsell_and_num = find_bestsell_and_num(my_id)
    #total_sales = find_today_total_sales(my_id)

    # return render_template('r_sell_list.html', data=get_order,acc=get_r_id(account))


@app.route('/restaurant_home')
def home2():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面
    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入

    get_order = r_getallList(my_id)
    total_sales = find_today_total_sales(my_id)
    total_orders = find_today_total_orders(my_id)
    finished_order = find_finished_order(my_id)
    bestsell_and_num = find_bestsell_and_num(my_id)
    find_comment = find_comments(my_id)
    #total_sales = find_today_total_sales(my_id)
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有購物車資料"  # 顯示提示訊息

    return render_template('home.html', data=get_order,acc=get_r_id(account),data2=total_sales,data3=total_orders,data4=finished_order,data5=bestsell_and_num,data6=find_comment)


@app.route('/restaurant_sell_list')
def restaurant_sell_list():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入

    get_order = r_getallList(my_id)
    #bestsell_and_num = find_bestsell_and_num(my_id)
    #total_sales = find_today_total_sales(my_id)
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有購物車資料"  # 顯示提示訊息

    return render_template('r_sell_list.html', data=get_order,acc=get_r_id(account))#,data5=bestsell_and_num

#外送員
@app.route('/delivery_home')
def home3():
    if 'loginAcc' not in session:
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    account = session['loginAcc']
    staff_data = get_d_id(account)

    global d_id
    d_id=staff_data
    if not d_id:
        return "找不到外送員資訊", 404  # 如果找不到該外送員，返回 404
    get_order = d_get_orderlist()
    # if not get_order:  # 如果 cart_data 是 None 或空
    #     get_order = "目前沒有待接訂單"  # 顯示提示訊息
    return render_template('d_status_and_getorder.html', data=get_order, acc=staff_data["d_account"], staff=staff_data)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 


@app.route('/privacy', methods=['GET'])
def privacy():
    # 獲取查詢參數 identity
    identity = request.args.get('identity')
    
    # 如果未提供身份，返回一個提示頁面或跳轉到註冊頁
    if not identity:
        return "未提供身份，請返回註冊頁面", 400
    # 渲染隱私頁面，並傳遞身份參數給模板
    return render_template('privacy.html', identity=identity)


# @app.route('/register_customer')
# def register_customer():
#     return render_template('c_register.html')

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        
        acc = request.form['acc']
        pwd = request.form['pwd']
        name = request.form['name']
        telephone = request.form['telephone']
        email = request.form['email']
        address = request.form['address']
        identity = "消費客戶"  # 設定身份為一般用戶
        
        add_customer_to_db(acc, pwd, name, telephone, email, address, identity)
        
        return redirect('/login_or_register')  # 假設註冊完成後導向登入頁面
    

    return render_template("c_register.html")

# @app.route('/register_restaurant')
# def register_restaurant():
#     return render_template('r_register.html') 

@app.route('/register_restaurant', methods=['GET', 'POST'])
def register_restaurant():
    if request.method == 'POST':
        
        r_account = request.form['r_account']
        r_pwd = request.form['r_pwd']
        r_name = request.form['r_name']
        r_phone = request.form['r_phone']
        r_addr = request.form['r_addr']
        r_time = request.form['r_time']
        identity = "餐廳業者"  # 設定身份為餐廳業者
        
        add_restaurant_to_db(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)

        return redirect('login_or_register')  # 假設註冊完成後導向 login 頁面
    
    # 如果是 GET 請求，則渲染註冊頁面
    return render_template("r_register.html")


# @app.route('/register_delivery')
# def register_delivery():
#     return render_template("d_register.html")

@app.route('/register_delivery', methods=['GET', 'POST'])
def register_delivery():
    if request.method == 'POST':
        # 從表單中獲取資料
        d_account = request.form['d_account']
        d_pwd = request.form['d_pwd']
        d_name = request.form['d_name']
        d_phone = request.form['d_phone']
        d_city = request.form['d_city']
        d_car = request.form['d_car']
        d_gmail = request.form['d_gmail']
        identity = request.form['identity']  # 這會是 "外送人員"
        
        add_deliverer_to_db(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity)

        return redirect('login_or_register') # 假設註冊完成後導向 home 頁面
    

    return render_template("d_register.html")


@app.route("/sales")
#使用server side render: template 樣板
def restaurant_sales():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入
    bestsell_and_num = find_bestsell_and_num(my_id)

    #total_sales = find_today_total_sales(my_id)
    # if not get_order:  # 如果 cart_data 是 None 或空
    #     get_order = "目前沒有購物車資料"  # 顯示提示訊息

    return render_template('r_salessummary.html',acc=get_r_id(account),data5=bestsell_and_num)


@app.route('/restaurant_turnover')
def restaurant_turnover():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id: 
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入
    get_information=find_r_turnover(my_id)
    get_information2=find_r_turnover_complete_order(my_id)

    return render_template('r_turnover.html', data=get_information,data2=get_information2)


@app.route('/restaurant_comment')
def restaurant_comment():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入
    find_comment = find_comments(my_id)
    #total_sales = find_today_total_sales(my_id)

    return render_template('r_comment.html',acc=get_r_id(account),data6=find_comment)


@app.route("/r_money")
def r_money():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入
    find_restaurant_info = find_r_information(my_id)

    #total_sales = find_today_total_sales(my_id)
    # if not get_order:  # 如果 cart_data 是 None 或空
    #     get_order = "目前沒有購物車資料"  # 顯示提示訊息

    return render_template('r_money.html',acc=get_r_id(account),data=find_restaurant_info)

@app.route('/update_restaurant/<int:r_id>', methods=['POST'])
def restaurant_update(r_id):  # 接收從 URL 傳遞過來的 r_id
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面
    
    form = request.form
    r_addr = form['r_addr']
    r_phone = form['r_phone']
    r_time = form['r_time']
    
    # 呼叫更新商家資料的函數
    update_restaurant_info(r_addr, r_phone, r_time, r_id)

    return redirect('/restaurant_manage')


@app.route('/restaurant_manage')#原先restaurant_home
def restaurant_manage():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]#字典轉變數
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")
    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入

    find_restaurant_info = find_r_information(my_id)
    #bestsell_and_num = find_bestsell_and_num(my_id)
    #total_sales = find_today_total_sales(my_id)

    return render_template('r_manage.html',acc=get_r_id(account),data=find_restaurant_info)#,data5=bestsell_and_num  
     

@app.route("/r_sell_food")
#使用server side render: template 樣板
def r_get_food():
	dat=r_getList(my_id)
	return render_template('r_sell_food.html',data=dat,id_in=my_id)

@app.route("/r_new")
#使用server side render: template 樣板
def r_add_new():

	return render_template('r_add_product.html')


# 設置上傳目錄
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
	return redirect(url_for('restaurant_sell_list'))

@app.route("/r_announced_deliver/<int:id>")
#使用server side render: template 樣板
def announced(id):
	dat=r_announced_deliver(id)
	return redirect(url_for('restaurant_sell_list'))

@app.route("/r_more_order_info/<int:col_id>")
#使用server side render: template 樣板
def r_more_order(col_id):
	data=r_getorderinfo(col_id)
	data_Dname=data[0]['Dname'].split(",")
	data_Num=data[0]['num'].split(",")
	data2=[]
	for i in range(len(data_Dname)):
		data2.append({
        'Dname': data_Dname[i].strip(),
        'num': int(data_Num[i].strip())
    })
    
	return render_template('r_more_order_info.html', data=data2)

# ____________________________________________________________________________________________________________________
#客戶註冊頁面
# @app.route("/") 
# def c_register(): 
# 	return render_template('c_register.html')

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
# @app.route("/c_home")
# def c_homepage():
# 	data=C_gethome()
# 	return render_template('c_homepage.html', data=data)

#條件搜尋(下拉)
@app.route("/search", methods=['get','post'])
def c_search():
    option=request.form.get('select')
    text=request.form.get('text')
    if (option!=None):
        data=C_gethome2(option, text)
        return render_template('c_homepage.html', data=data)
    elif(text!=""):
        data=C_gethome2(option, text)
        return render_template('c_homepage.html', data=data)
    else:
        data=C_gethome()
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
@app.route("/c_addcar/<string:Rname>/<int:Rid>/<string:Dname>/<int:Dprice>/<int:Num>/<int:Sum>/<int:Mid>")
def c_addtocar(Rname, Rid, Dname, Dprice, Num, Sum, Mid):
	data=C_getmenu(Rid)
	fbdata=C_getfeedback(Rid)
	C_addcar(Rname, Dname, Dprice, Num, Sum)
	return render_template('c_Rmanu.html', data=data, Rname=Rname, Rid=Rid, fbdata=fbdata, Mid=Mid)

#購物車
@app.route("/c_car/<string:Rname>/<int:Rid>/<int:Mid>")
def c_showcar(Rname, Rid, Mid):
	data=C_getcar(Rname)
	total=C_getcartotal(Rname)['total']
	return render_template('c_carlist.html', data=data, Rname=Rname, total=total, Rid=Rid, Mid=Mid)

#購物車：移除
@app.route("/c_delcar/<string:Rname>/<int:Rid>/<string:Dname>")
def c_rmcar(Rname, Rid, Dname):
	C_removecar(Rname, Dname)
	data=C_getcar(Rname)
	total=C_getcartotal(Rname)['total']
	return render_template('c_carlist.html', data=data, Rname=Rname, total=total, Rid=Rid)

#下單
@app.route("/c_addorder/<string:Rname>/<int:Rid>/<int:Mid>")
def c_addorder(Rname, Rid, Mid):
	C_addorder(Rname, Rid, Mid, my_id)
	data=C_gethome()
	return render_template('c_homepage.html', data=data)

#已下定清單
@app.route("/c_orderlist")
def c_Olist():
	data=C_getorderlist()
	return render_template('c_orderlist.html', data=data)

#已下定清單詳細內容
@app.route("/c_orderlistinfo/<string:Rname>/<int:Oid>")
def c_Olistinfo(Rname, Oid):
	data=C_getorderinfo(Rname, Oid)
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
	msg=C_getbtntext(statusid)
	return render_template('c_orderlistinfo.html', Rname=Rname, sum=sum, status=status, data2=data2, msg=msg, Oid=Oid)

#取消訂單/收貨確認
@app.route("/c_recievecheck/<string:Rname>/<string:msg>/<int:Oid>")
def c_check(Rname, msg, Oid):
	if msg=="取消訂單":
		C_getbtnfunc(Oid)
		data=C_gethome()
		return render_template('c_homepage.html', data=data)
	else:
		return render_template('c_recievecheck.html', Rname=Rname, Oid=Oid)
	
#不予評價
@app.route("/c_feedbackNUPL/<int:Oid>")
def c_nofeedback(Oid):
	C_getbtnfunc(Oid)
	data=C_gethome()
	return render_template('c_homepage.html', data=data)

#前往給予評價
@app.route("/c_feedbackUPL/<string:Rname>/<int:Oid>")
def c_feedback(Rname, Oid):
	C_getbtnfunc(Oid)
	return render_template('c_feedbackUPL.html', Rname=Rname)

#確實給予評價
@app.route("/c_insertfeedback/<string:Rname>", methods=['get','post'])
def c_insertfb(Rname):
	comment=request.form.get('feedback')
	rating=request.form.get('rating')
	rid=C_getrid(Rname)['rid']
	C_insertfb(rid, rating, comment)
	data=C_gethome()
	return render_template('c_homepage.html', data=data)


# ________________________________________________________________________________________________________________
#外送員開始#


@app.route('/delivery_status/<int:d_sid>')
@login_confirm_acc_and_pwd #上鎖
def delivery_status(d_sid):
    # 使用 d_sid 從資料庫取得外送員資訊
    staff_data = get_delivery_staff(d_sid)
    
    if not staff_data:
        return "找不到外送員資訊", 404  # 如果找不到該外送員，返回 404

    # 將資料傳遞到 HTML 模板中
    return render_template('d_status_and_getorder.html', staff=staff_data)

# @app.route('/get_price/<int:o_id>/staff/<int:d_sid>') #取得餐點金額
# @login_confirm_acc_and_pwd #上鎖
# def get_price(o_id):
#     # 使用 d_sid 從資料庫取得外送員資訊
#     account = session['loginAcc']
#     staff_data = get_d_id(account)  
#     get_price=d_getp(o_id)
#     return render_template('d_status_and_getorder.html', staff=staff_data)

@app.route('/delivery_status/online/<int:d_sid>')
@login_confirm_acc_and_pwd #上鎖
def d_update_status_to_online(d_sid):
    # 使用 d_sid 從資料庫取得外送員資訊
    d_status(d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)  
    get_order = d_get_orderlist()
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有待接訂單"  # 顯示提示訊息
    return render_template('d_status_and_getorder.html', data=get_order, acc=staff_data["d_account"], staff=staff_data)


@app.route('/delivery_status/offline/<int:d_sid>')
@login_confirm_acc_and_pwd #上鎖
def d_update_status_to_offline(d_sid):
    # 使用 d_sid 從資料庫取得外送員資訊
    d_status_out(d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)  
    get_order = d_get_orderlist()
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有待接訂單"  # 顯示提示訊息
    return render_template('d_status_and_getorder.html', data=get_order, acc=staff_data["d_account"], staff=staff_data)

#
@app.route('/order_status/<int:o_id>/delivery/<int:d_sid>') #轉到pickup.html
@login_confirm_acc_and_pwd #上鎖
def d_get_order(o_id, d_sid): #訂單已取
    d_change_staff_status(d_sid)
    d_change_order_statusto3(o_id, d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)
    get_order = d_find_taked_order(d_sid) 
    r_id = get_order["r_id"]
    restaurant = d_rinformation(r_id)
    c_id = get_order["c_id"]
    customer = d_cinformation(c_id)
    return render_template('track.html', data=get_order, restaurant=restaurant, acc=staff_data["d_account"], staff=staff_data ,customer=customer)

# @app.route('/order_status/arrive1/<int:o_id>/delivery/arrive1/<int:d_sid>') #取到餐
# @login_confirm_acc_and_pwd #上鎖
# def d_arrive1(o_id, d_sid): 
#     #d_change_order_statusto4(o_id, d_sid)
#     account = session['loginAcc']
#     staff_data = get_d_id(account)
#     get_order = d_find_arrived_order(d_sid)
#     c_id = get_order["c_id"]
#     customer = d_cinformation(c_id)
#     return render_template('pickup.html', data=get_order, customer=customer, acc=staff_data["d_account"], staff=staff_data)

# @app.route('/order_status/arrive2/<int:d_sid>') #取到餐
# @login_confirm_acc_and_pwd #上鎖
# def d_arrive2(d_sid): 
#     account = session['loginAcc']
#     staff_data = get_d_id(account)
#     get_order = d_find_arrived_order(d_sid)
#     c_id = get_order["c_id"]
#     customer = d_cinformation(c_id)
#     return render_template('arrive.html', data=get_order, customer=customer, acc=staff_data["d_account"], staff=staff_data)

@app.route('/order_status/finish/<int:o_id>/delivery/finish/<int:d_sid>') #抵達客戶地址 完成定單
@login_confirm_acc_and_pwd #上鎖
def d_finish(o_id, d_sid): 
    d_change_order_statusto5(o_id, d_sid)
    d_status(d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)
    get_order = d_find_finished_order(d_sid)
    return render_template('finish.html', data=get_order, acc=staff_data["d_account"], staff=staff_data)

@app.route('/delivery_record/<int:d_sid>')
def d_record(d_sid):
    if 'loginAcc' not in session:
        return render_template('login_or_register.html') 
    account = session['loginAcc']
    staff_data = get_d_id(account)
    get_order = d_getrecord(d_sid)
# 顯示提示訊息
    return render_template('d_record.html', data=get_order, staff=staff_data,)

@app.route('/track_order_status/<int:d_sid>')
def track_order_status(d_sid):
    if 'loginAcc' not in session:
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面

    # 獲取登入用戶的資料
    account = session['loginAcc']
    staff_data = get_d_id(account)  # 獲取外送人員資料
    d_sid = staff_data["d_sid"]  # 登入者的 d_sid

    # 查詢該 d_sid 接的訂單
    orders = d_get_order_status(d_sid)  # 返回該外送人員的所有訂單
    if not orders:
        return render_template('no_order.html', staff=staff_data)    # 若該外送人員沒有訂單，顯示提示訊息

    # 假設這裡只取第一個訂單
    o_id = orders["o_id"]
    o_status = orders["o_status"]

    # 根據訂單狀態顯示相應的頁面
    if o_status == 3 or 4:
        return  redirect(url_for('d_get_order', o_id=o_id, d_sid=d_sid))
    # elif o_status == 4:
    #     return  redirect(url_for('d_arrive', o_id=o_id, d_sid=d_sid))
    elif o_status == 5:
        return  redirect(url_for('home3', o_id=o_id, d_sid=d_sid))
    else:
        return "未知的訂單狀態，請聯繫管理員"
    

@app.route('/delivery_other_info')
def delivery_other_info():
    # 檢查用戶是否已登入
    if 'loginAcc' not in session:
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    
    account = session['loginAcc']  
    get_d_sid = get_dsid(account)
    
    getdsid = get_d_sid['d_sid']
    print(getdsid,"7777")

    order = order_info(getdsid)  # 返回的是字典形式的訂單資料
    goodrate = count_delivery_goodrate(getdsid)  
    total_order = total_order_info(getdsid)
    return render_template('deliverhome.html', data=goodrate,orders=order,total_order=total_order)



#_______________________________________________________________________________________________________________
# @app.route('/test')
# def show_list():
#     data_test = [
#         {"name":'這是名子',"content":'這是內容',"price":'還有這個是底價'}
#     ]
#     return render_template('home.html',data=data_test)
    
# @app.route('/login' , methods= ['POST','GET'])
# def login():
#     if request.method == 'POST':
#         form = request.form
#         acc = form['Account']
#         pwd = form['Password']
#         # check if the acc and pwd both are right
#         if acc =='123' and pwd =='456':
#             session['acc'] = acc
#             return redirect("/home")
#         else:
#             session['acc'] = False
#             return redirect('/login')
#     else:
#         return render_template('login.html')
    
# @app.route('/home')
# def home():
#     dat=get_product_from_sql()
#     return render_template('home.html',data=dat)

# @app.route('/test')
# def show_list():
#     data_test = [
#         {"name":'這是名子',"content":'這是內容',"price":'還有這個是底價'}
#     ]
#     return render_template('home.html',data=data_test)

# @app.route('/add_new_product', methods=['POST','GET'])
# def add_new_product():
#     if request.method =='POST':
#         pro_id = request.form.get('pro_id')
#         pro_name = request.form.get('pro_name')
#         pro_content = request.form.get('pro_content')
#         pro_price = request.form.get('pro_price')

#         if not pro_name or not pro_content or not pro_price:
#             error = '所有欄位為必填'
#             return render_template('add_product.html',error=error)
#         add_product_to_sql(pro_name,pro_content,pro_price)
#         return redirect("/listProduct")
#     else:
#         return render_template('add_product.html')

# @app.route('/listProduct')
# def gl():
#     dat=get_product_from_sql()
#     return render_template('home.html',data=dat)


# @app.route('/delete_product', methods=['POST'])
# def delete_product():
#     pro_name = request.form.get('pro_name') 
#     if pro_name:
#         delete_product_from_sql(pro_name) 
#     return redirect('/listProduct')

# @app.route('/update_product', methods=['POST'])
# def update_product():
#     pro_name = request.form.get('pro_name')
#     new_pro_content = request.form.get('new_pro_content')
#     new_pro_price = request.form.get('new_pro_price')
    
#     if pro_name and new_pro_content and new_pro_price:
#         update_product_from_sql(pro_name, new_pro_content, new_pro_price)
#         return redirect('/listProduct')
    
#     # 如果沒有完整資料或需要重新渲染表單，獲取特定商品資料
#     product = get_product_from_sql(pro_name)  # 傳遞商品名稱
#     return render_template('update_product.html', data=[product])

