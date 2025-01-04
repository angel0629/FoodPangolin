from flask import Flask , render_template ,request , session , redirect,url_for
from functools import wraps
import os
from Database import d_get_order_status,d_getrecord,d_find_finished_order, d_cinformation, d_find_arrived_order, d_rinformation, d_find_taked_order, d_change_order_statusto5 ,d_change_order_statusto4, d_change_order_statusto3,d_change_staff_status,d_status_out,d_status,d_get_orderlist,get_d_id,get_delivery_staff,get_users_from_db,get_customer_cart_from_sql,add_deliverer_to_db,add_customer_to_db,add_restaurant_to_db,r_getList, r_add, r_editList, r_update, r_delete , r_getallList,r_acceptList,r_announced_deliver,get_r_id
#app = Flask(__name__ , static_folder = 'static' , static_url_path = '/')
app = Flask(__name__ , static_folder = 'static')
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
                return redirect("/customer_home")  # 跳轉到消費者主頁
            elif identity == '餐廳業者':
                return redirect('/restaurant_home')  # 跳轉到餐廳業者主頁
            elif identity == '外送人員':
                return redirect('/delivery_home')  # 跳轉到外送員主頁
            else:
                return redirect('/home')  # 預設主頁（如果身份不正確）
        else:
            error = '帳號或密碼輸入錯誤'
            return render_template('login_or_register.html', error=error)  # 傳遞錯誤訊息

    # 如果是 GET 請求，顯示登錄頁面
    return render_template('login_or_register.html')



@app.route('/customer_home')
def home1():
    if 'loginAcc' not in session:
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    
    account = session['loginAcc']
    cart_data = get_customer_cart_from_sql(account, cart_id=1)
    if not cart_data:  # 如果 cart_data 是 None 或空
        cart_data = "目前沒有購物車資料"  # 可以顯示一個提示訊息

    return render_template('user_home2.html', data=cart_data)


@app.route('/restaurant_home')
def home2():
    if 'loginAcc' not in session:
        return redirect('/login_or_register')  # 未登入時重定向到登入頁面

    account = session['loginAcc']
    my_id_dict = get_r_id(account)
    global my_id
    my_id=my_id_dict["r_id"]
    #app.logger.info(f"查詢帳號 {account} 的 r_id: {my_id}")

    
    if not my_id:  # 如果 my_id 是 None，表示查詢失敗
        return "查無此帳號，請重新登入", 403  # 回應 403 Forbidden 或引導至登入

    get_order = r_getallList(my_id)
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有購物車資料"  # 顯示提示訊息

    return render_template('r_sell_list.html', data=get_order,acc=get_r_id(account))

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
        # 從表單中獲取資料
        acc = request.form['acc']
        pwd = request.form['pwd']
        name = request.form['name']
        telephone = request.form['telephone']
        email = request.form['email']
        address = request.form['address']
        identity = "消費客戶"  # 設定身份為一般用戶
        
        # 呼叫函數來插入資料
        add_customer_to_db(acc, pwd, name, telephone, email, address, identity)
        
        # 完成後導向到登入頁或其他頁面
        return redirect('/login_or_register')  # 假設註冊完成後導向登入頁面
    
    # 如果是 GET 請求，則渲染註冊頁面
    return render_template("c_register.html")

# @app.route('/register_restaurant')
# def register_restaurant():
#     return render_template('r_register.html') 

@app.route('/register_restaurant', methods=['GET', 'POST'])
def register_restaurant():
    if request.method == 'POST':
        # 從表單中獲取資料
        r_account = request.form['r_account']
        r_pwd = request.form['r_pwd']
        r_name = request.form['r_name']
        r_phone = request.form['r_phone']
        r_addr = request.form['r_addr']
        r_time = request.form['r_time']
        identity = "餐廳業者"  # 設定身份為餐廳業者
        
        # 呼叫函數來插入資料
        add_restaurant_to_db(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)
        # 完成後導向至其他頁面，例如登入頁
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
        
        # 呼叫資料庫函數來插入資料
        add_deliverer_to_db(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity)
        # 完成後導向至其他頁面，例如首頁或登入頁
        return redirect('login_or_register') # 假設註冊完成後導向 home 頁面
    
    # 如果是 GET 請求，則渲染註冊頁面
    return render_template("d_register.html")


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
	return redirect(url_for('home2'))

@app.route("/r_announced_deliver/<int:id>")
#使用server side render: template 樣板
def announced(id):
	dat=r_announced_deliver(id)
	return redirect(url_for('home2'))

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


@app.route('/order_status/<int:o_id>/delivery/<int:d_sid>') #接訂單
@login_confirm_acc_and_pwd #上鎖
def d_get_order(o_id, d_sid): #訂單已取
    d_change_staff_status(d_sid)
    d_change_order_statusto3(o_id, d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)
    get_order = d_find_taked_order(d_sid)
    r_id = get_order["r_id"]
    restaurant = d_rinformation(r_id)
    return render_template('pickup.html', data=get_order, restaurant=restaurant, acc=staff_data["d_account"], staff=staff_data)

@app.route('/order_status/arrive/<int:o_id>/delivery/arrive/<int:d_sid>') #取到餐
@login_confirm_acc_and_pwd #上鎖
def d_arrive(o_id, d_sid): 
    d_change_order_statusto4(o_id, d_sid)
    account = session['loginAcc']
    staff_data = get_d_id(account)
    get_order = d_find_arrived_order(d_sid)
    c_id = get_order["c_id"]
    customer = d_cinformation(c_id)
    return render_template('arrive.html', data=get_order, customer=customer, acc=staff_data["d_account"], staff=staff_data)

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
        return render_template('login_or_register.html')  # 如果未登入，跳轉到登入頁面
    account = session['loginAcc']
    staff_data = get_d_id(account)

    get_order = d_getrecord(d_sid)
    if not get_order:  # 如果 cart_data 是 None 或空
        get_order = "目前沒有接單紀錄"  # 顯示提示訊息
    return render_template('d_record.html', data=get_order, staff=staff_data,)

@app.route('/logout', methods=['GET'])
def logout():
    # 清除 session 中的用戶資料
    session.pop('loginAcc', None)
    
    # 跳轉到登錄頁面
    return render_template('/login_or_register')

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
    if o_status == 3:
        return  redirect(url_for('d_get_order', o_id=o_id, d_sid=d_sid))
    elif o_status == 4:
        return  redirect(url_for('d_arrive', o_id=o_id, d_sid=d_sid))
    elif o_status == 5:
        return  redirect(url_for('home3', o_id=o_id, d_sid=d_sid))
    else:
        return "未知的訂單狀態，請聯繫管理員"

