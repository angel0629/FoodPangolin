from flask import Flask, session, redirect, render_template,request,flash
from functools import wraps
from dbUtils import add_delivery,get_order
import dbUtils as DB

                                    #/會導到  static
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
#app.config['SECRET_KEY'] = '123TyU%^&'  #不知為何沒用
app.secret_key = 'your_secret_key'  # 設置 session 的密鑰


@app.route('/')
def home():
    return render_template('loginPage.html')

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
    return render_template('loginPage.html') 

@app.route('/login', methods=['POST'])
def login():
	form =request.form
	id = form['ID']
	pwd =form['PWD']
	userData=DB.checkLogin(id,pwd)
	if userData:
		session['loginID']=userData['ID']
		return redirect("/")
	else:
		session['loginID']=0
		return redirect("/loginPage")

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/add_delivery', methods=['POST'])
def d_register():
    try:
        # 接收來自 HTML 表單的資料
        d_account = request.form.get('ID')  # 對應前端表單的 name="ID"
        d_pwd = request.form.get('PWD')    # name="PWD"
        d_city = request.form.get('city')  # name="city"
        d_car = request.form.get('car')    # name="car"
        d_name = request.form.get('name')  # name="name"
        d_phone = request.form.get('phone')  # name="phone"
        d_gmail = request.form.get('gmail')  # name="gmail"
        # 打印日誌確認表單資料是否正確
        print(f"Received data: {d_account}, {d_pwd}, {d_city}, {d_car}, {d_name}, {d_phone}, {d_gmail}")
        
        # 驗證資料
        if not d_account or not d_pwd or not d_city:
            flash('缺少必要資料', 'error')
            return redirect('/register')

        # 插入資料
        
        DB.add_delivery(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail)

        flash('註冊成功！', 'success')
        return redirect('/')
    except Exception as e:
        print(f"Error occurred during registration: {e}")
        flash('註冊失敗，請稍後重試！', 'error')
        return redirect('/register')

@app.route("/order") 
@login_required
def d_orderinformation():
	dat=DB.get_order()
	return render_template('order.html', data=dat) 



"""
@app.route("/detail") 
@login_required
def orderdetail():
	dat=get_detail()
	return render_template('detail.html', data=dat) 
"""