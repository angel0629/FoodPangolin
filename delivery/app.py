from flask import Flask, session, redirect, flash ,render_template,request 
from functools import wraps
from dbUtils import get_detail,get_order,getdetail,get_user,get_status,get_person_product,addtodb,getlist,deleteproduct,insert_bid,update_item_description #import dbUtils 並得到 getList 這個指令

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
#app.config['SECRET_KEY'] = '123TyU%^&'  不知為何沒用
app.secret_key = 'your_secret_key'  # 設置 session 的密鑰


# 驗證登入狀態的裝飾器
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs): #wrapper 函式是 login_required 裝飾器中的內部函式。它包裹了被裝飾的函式 f
        loginID = session.get('loginID')#session 是 Flask 用來儲存使用者資訊的物件
        if not loginID:
            return redirect('/loginPage')  # 重定向到 /loginPage
        return f(*args, **kwargs)
    return wrapper


# 顯示登入頁面的路由
@app.route('/loginPage', methods=['GET'])
def login_page():
    return render_template('loginPage.html')  # 顯示 loginPage.html

# 處理登入
@app.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form['ID']
    password = form['PWD']

    # 使用 db.py 中的函數來查找用戶
    user = get_user(username, password)

    if user:
        session['loginID'] = user['user_id']  # 使用 user_id 來標識登入的用戶
        return redirect("/")
    else:
        session['loginID'] = False
        return redirect("/loginPage")  # 如果登入失敗，重定向到 /loginPage

@app.route("/status")  #個人商品
@login_required
#使用server side render: template 樣板
def my():
    user_id = session.get('loginID')  # 獲取當前登入使用者的 ID
    dat = get_status(user_id)  # 傳入 user_id 查詢該使用者的產品
    return render_template('statusUI.html', data=dat)

@app.route("/order") 
@login_required
def shopinformation():
	dat=get_order()
	return render_template('order.html', data=dat) 

@app.route("/detail") 
@login_required
def orderdetail():
	dat=get_detail()
	return render_template('detail.html', data=dat) 



