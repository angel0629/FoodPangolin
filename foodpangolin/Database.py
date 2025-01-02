import mysql.connector

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port="3306",
        database="foodpangolin"
    )
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as e:
    print(e)
    print("error connecting to DB")
    exit(1)

def get_users_from_db(account, password, identity):
    if identity == '消費客戶':  # 查詢消費者資料
        sql = "SELECT * FROM client_account where client_account.ca_Acc = %s AND ca_Psw = %s"
    elif identity == '餐廳業者':  # 查詢餐廳業者資料
        sql = "SELECT r_id FROM restaurant WHERE r_account = %s AND r_pwd = %s ;"  
    elif identity == '外送人員':  # 查詢外送員資料
        sql = "SELECT * FROM delivery_staff WHERE d_account = %s AND d_pwd = %s;" 
    else:
        return None  # 如果身份不正確，返回None

    param = (account, password)
    cursor.execute(sql, param)
    user = cursor.fetchone()  # 獲取單一結果
    return user  # 返回查詢結果


def get_restaurant_from_db(acc):
    sql = 'SELECT * FROM restaurant WHERE acc = %s;'
    param = (acc,)  # 加上逗號，確保這是一個元組
    cursor.execute(sql, param)
    user = cursor.fetchone()  # 獲取單一結果
    return user  # 返回用戶資料


# def get_customer_cart_from_sql(acc, cart_id=1):
#     if cart_id:
#         # 把customer跟cart找出來
#         sql = "SELECT * FROM cart INNER JOIN customer ON cart.c_id = customer.c_id AND customer.acc = %s AND cart.cart_id = %s;"
#         param = (acc, cart_id)  # 正確的參數順序
#         cursor.execute(sql, param)
#         return cursor.fetchone()  # 返回單一商品資料
#     else:
#         # 查詢所有商品
#         sql = "SELECT * FROM cart;"
#         cursor.execute(sql)
#         return cursor.fetchall()  # 返回所有商品資料


def get_customer_cart_from_sql(acc):
    # 把customer跟cart找出來
    sql = "SELECT * FROM client_account where client_account.ca_Acc = %s;"
    param = (acc,)  # 正確的參數順序
    cursor.execute(sql, param)
    return cursor.fetchone()  

    
    
def add_deliverer_to_db(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity):
    sql = "INSERT INTO delivery_staff(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, d_status, identity)VALUES (%s, %s, %s, %s, %s, %s, %s, '空閒', %s)"
    param = (d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity)
    cursor.execute(sql, param)
    conn.commit()
    return

# def add_customer_to_db(acc, pwd, name, telephone, email, address, identity):
#     sql = "INSERT INTO customer(acc, pwd, name, telephone, email, address, identity)VALUES(%s, %s, %s, %s, %s, %s, %s)"
#     param = (acc, pwd, name, telephone, email, address, identity)
#     cursor.execute(sql, param)
#     conn.commit()
#     return

def add_customer_to_db(acc, pwd, fname, lname, telephone, email, address):
    sql = """
    INSERT INTO customer(ca_Acc, ca_Psw, ca_FName, ca_LName, ca_Tel, ca_Email, ca_Add, identity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    param = (acc, pwd, fname, lname, telephone, email, address, '消費客戶')
    cursor.execute(sql, param)
    conn.commit()
    return


def add_restaurant_to_db(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity):
    sql = "INSERT INTO restaurant(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)VALUES (%s, %s, %s, %s, %s, %s, %s);"
    param = (r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)
    cursor.execute(sql, param)
    conn.commit()
    return
#找出今日營業額 chrisluo
def find_today_total_sales(r_id):
    sql = "SELECT sum(m_price) as total_sales FROM `menu` WHERE r_id=%s;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出該餐廳有多少餐點被下訂 chrisluo
def find_today_total_orders(r_id):
    sql = "SELECT COUNT(o_id) AS total_orders FROM `orders` WHERE r_id = %s;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出status=5，已完成訂單 chrisluo
def find_finished_order(r_id):
    sql = "SELECT COUNT(orders.o_status) AS completed_orders FROM orders INNER JOIN status ON orders.o_status = status.status_id WHERE orders.r_id = %s AND status.status_id = 5;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出明星商品跟銷售數量chrisluo
def find_bestsell_and_num(r_id):
    sql = "select menu.m_name,menu.order_count from menu where menu.r_id=%s group by menu.order_count Desc;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result
#抓出客戶評論chrisluo
def find_comments(r_id):
    sql='select r_star.comments,r_star.c_id,r_star.rating from r_star where r_id = %s;'
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result

#抓出turnover資料chrisluo
def find_r_turnover(r_id):
    sql='SELECT orders.o_id, orders.pickup_time, menu.m_detail, menu.m_price, menu.m_id AS menu_item_id,status.status_name FROM orders INNER JOIN menu ON orders.m_id = menu.m_id INNER JOIN status ON orders.o_status = status.status_id WHERE orders.r_id = %s AND status.status_id = 2 ORDER BY orders.pickup_time DESC, orders.o_id ASC;'
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result

def find_r_turnover_complete_order(r_id):
    sql='SELECT SUM(menu.m_price) AS total_revenue, COUNT(*) AS completed_orders FROM orders INNER JOIN menu ON orders.m_id = menu.m_id INNER JOIN status ON orders.o_status = status.status_id WHERE orders.r_id = %s AND status.status_id = 5;'
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result

def find_r_information(r_id):
    sql='SELECT * FROM `restaurant` WHERE r_id=%s;'
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result

def update_restaurant_info(r_addr,r_phone,r_time,r_id,):
    sql='UPDATE restaurant SET r_addr = %s, r_phone = %s, r_time = %s WHERE r_id = %s'
    param = (r_addr,r_phone,r_time,r_id,)  
    cursor.execute(sql, param)
    conn.commit()
    
#新增產品
def r_add(name,price,more,picture,my_id):
	#在自己的上架清單新增上架
	sql="INSERT INTO `menu` (`m_id`, `m_name`, `m_price`, `m_detail`, `m_picture`, `r_id`) VALUES (NULL, %s, %s, %s, %s, %s);"
	param=(name,price,more,picture,my_id)
	cursor.execute(sql,param)
	'''
	s_id = cursor.lastrowid

	#在所有的上架清單中新增	
	sql2="INSERT INTO `all_sells` (`id`, `s_id`, `price`, `u_id`) VALUES (NULL, %s, %s, %s);"
	param2=(s_id,price,'底價')#標記為底價
	cursor.execute(sql2,param2)
	'''
	#因為s_id為NULL，所以要分兩個Insert


	conn.commit()

#刪除商品
def r_delete(id):
	sql="DELETE FROM `menu` WHERE `menu`.`m_id` = %s;"
	cursor.execute(sql,(id,))
	conn.commit()

#更新上架商品
def r_update(name,price,detail,picture,edit_id):
	#更新自己的上架清單
	sql="UPDATE `menu` SET `m_name` = %s, `m_price` = %s, `m_detail` = %s, `m_picture` = %s WHERE `menu`.`m_id` = %s"
	param=(name,price,detail,picture,edit_id)
	cursor.execute(sql,param)

	conn.commit()

#更改產品內容
def r_editList(id):
	sql="""SELECT menu.m_name, menu.m_price, menu.m_detail, menu.m_picture 
			FROM `menu` 
			WHERE menu.m_id=%s;"""

	cursor.execute(sql,(id,))
	return cursor.fetchall()

#顯示自己上架清單
def r_getList(my_id):
	sql="""SELECT menu.m_id, menu.m_name, menu.m_price, menu.m_picture, menu.m_detail
			FROM `menu` 
			WHERE menu.r_id=%s
            """

	cursor.execute(sql,(my_id,))
	return cursor.fetchall()


#顯示所有訂單清單
def r_getallList(my_id):
	try:
		#連線DB
		conn = mysql.connector.connect(
			user="root",
			password="",
			host="localhost",
			port=3306,
			database="foodpangolin"
		)
		#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
		cursor=conn.cursor(dictionary=True)
	except mysql.connector.Error as e: # mariadb.Error as e:
		print(e)
		print("Error connecting to DB")
		exit(1)
	sql="""SELECT orders.o_id, customer.name,delivery_staff.d_name, orders.pickup_time, orders.delivery_time, orders.o_status
		FROM orders INNER JOIN customer ON orders.c_id=customer.c_id
		INNER JOIN delivery_staff ON orders.d_sid=delivery_staff.d_sid
		INNER JOIN restaurant ON orders.r_id=restaurant.r_id
		WHERE restaurant.r_id=%s;"""
	cursor.execute(sql,(my_id,))
	return cursor.fetchall()

def r_acceptList(o_id):
	sql="UPDATE `orders` SET `o_status` = %s WHERE `orders`.`o_id` = %s"
	param=("已接單",o_id)
	cursor.execute(sql,param)
	conn.commit()

def r_announced_deliver(o_id):
	sql="UPDATE `orders` SET `o_status` = %s WHERE `orders`.`o_id` = %s"
	param=("配送中",o_id)
	cursor.execute(sql,param)
	conn.commit()
def get_r_id(account):
	sql="""SELECT restaurant.r_id From restaurant where r_account=%s
            """

	cursor.execute(sql,(account,))
	return cursor.fetchone()      

# _________________________________________________________________________________________________________________________
#客戶註冊資料儲存至DB
def C_insertacc(acc, psw, fname, lname, tel, email, add):
	sql="insert into Client_account (ca_Acc, ca_Psw, ca_FName, ca_LName, ca_Tel, ca_Email, ca_Add) value(%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(sql, (acc, psw, fname, lname, tel, email, add))
	conn.commit()
	return

#取得客戶資訊
def C_getuser(cid):
	sql="SELECT ca_FName Cfname FROM client_account WHERE client_account.ca_Id=%s"
	cursor.execute(sql, (cid,))
	return cursor.fetchone()

#取得homepage
def C_gethome():
	sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  rid;"
	cursor.execute(sql)
	return cursor.fetchall()

#取得條件篩選排列的homepage
def C_gethome2(option, text):
	if (text != ""):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id  AND restaurant.r_name LIKE %s;"
		cursor.execute(sql,(text,))
		return cursor.fetchall()

	if (option=="1"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg ASC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="2"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="3"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY rating ASC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="4"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()

#取得各餐廳menu
def C_getmenu(Rid):
	sql="SELECT m_id mid, m_name name, m_price price, m_picture pic FROM menu WHERE r_id=%s;"
	cursor.execute(sql,(Rid,))
	return cursor.fetchall()

#取得各餐廳feedback
def C_getfeedback(Rid):
	sql="SELECT (SELECT ca_Fname FROM client_account WHERE r_star.ca_Id = client_account.ca_Id )user , rating, comments feedback FROM r_star WHERE r_star.r_id = %s;"
	cursor.execute(sql, (Rid,))
	return cursor.fetchall()

#取得菜單詳細資訊
def C_getmenuinfo(Rid, Mid):
	sql="SELECT m_id mid, m_name name, m_price price, m_detail detail, m_picture pic FROM menu WHERE r_id=%s AND m_id=%s;"
	cursor.execute(sql, (Rid, Mid,))
	return cursor.fetchone()

#加入購物車
def C_addcar(Rname, Dname, Dprice, Num, Sum):
	sql="insert into Client_carlist (r_name, ca_Id, ccl_DName, ccl_Dprice, ccl_Num, ccl_Sum) value(%s,%s,%s,%s,%s,%s);"
	cursor.execute(sql, (Rname, 1, Dname, Dprice, Num, Sum,))
	conn.commit()
	return

#取得購物車清單
def C_getcar(Rname):
	sql="SELECT ccl_DName Dname, ccl_DPrice Dprice, ccl_Num num, ccl_Sum sum FROM client_carlist WHERE r_name=%s;"
	cursor.execute(sql, (Rname,))
	return cursor.fetchall()

#取得購物車總金額
def C_getcartotal(Rname):
	sql="SELECT SUM(ccl_Sum) total FROM client_carlist WHERE r_name=%s;"
	cursor.execute(sql, (Rname,))
	data=cursor.fetchone()
	if data['total']!=None:
		return data
	else:
		data['total']= 0
		return data
	
#自購物車移除
def C_removecar(Rname, Dname):
	sql="Delete FROM client_carlist WHERE r_name=%s AND ccl_DName=%s;"
	cursor.execute(sql, (Rname, Dname,))
	conn.commit()
	return

#下單
def C_addorder(Rname):
	sql="INSERT INTO Client_orderlist (col_RName, col_DName, col_Num, col_DPrice, col_Sum) SELECT r_name, GROUP_CONCAT(ccl_DName SEPARATOR ', '), GROUP_CONCAT(ccl_Num SEPARATOR ', '), GROUP_CONCAT(ccl_Sum SEPARATOR ', '), sum(ccl_Sum) FROM client_carlist WHERE client_carlist.r_name=%s;"
	cursor.execute(sql, (Rname,))
	conn.commit()
	sql1=sql="Delete FROM client_carlist WHERE r_name=%s;"
	cursor.execute(sql1, (Rname,))
	conn.commit()
	return

#取得訂單列表
def C_getorderlist():
	sql="SELECT col_Id Oid, col_RName Rname, col_Sum sum FROM client_orderlist;"
	cursor.execute(sql)
	return cursor.fetchall()

#取得訂單詳細內容
def C_getorderinfo(Rname, Oid):
	sql="SELECT col_RName Rname, col_DName Dname, col_DPrice Dprice, col_Num num, col_Sum sum, col_status status FROM client_orderlist WHERE client_orderlist.col_RName=%s AND client_orderlist.col_Id=%s"
	cursor.execute(sql, (Rname, Oid,))
	return cursor.fetchall()

#取得訂單狀態
def C_getstatus(statusid):
	sql="SELECT status_name status FROM status WHERE status.status_id=%s"
	cursor.execute(sql, (statusid,))
	return cursor.fetchone()

#取得對應按鈕text
def C_getbtntext(statusid):
	if statusid==1:
		msg="取消訂單"
	else:
		msg="確認收貨"
	return msg

#取得按鈕功能
def C_getbtnfunc(Oid):
	sql="Delete FROM client_orderlist WHERE client_orderlist.col_Id=%s;"
	cursor.execute(sql, (Oid,))
	conn.commit()
	return

#取得rid
def C_getrid(Rname):
	sql="SELECT r_id rid FROM restaurant WHERE restaurant.r_name=%s"
	cursor.execute(sql, (Rname, ))
	return cursor.fetchone()

#新增評論至DB
def C_insertfb(rid, rating, comment):
	sql="INSERT INTO r_star (ca_Id, r_id, rating, comments) VALUE(%s, %s, %s, %s);"
	cursor.execute(sql, (1, rid, rating, comment,))
	conn.commit()
	return 
# def add_product_to_sql(pro_name,pro_content,pro_price):
#     # 資料庫語句，後面的值也是資料庫中項目的名子
#     sql="insert into product_list (pro_name,pro_content,pro_price) VALUES (%s,%s,%s) " 
#     param=(pro_name,pro_content,pro_price)
#     cursor.execute(sql,param)
#     conn.commit()
#     return




# def delete_product_from_sql(pro_name):
#     sql = "DELETE FROM product_list WHERE pro_name = %s"
#     cursor.execute(sql, (pro_name,)) 
#     conn.commit()
#     return

# def update_product_from_sql(pro_name,new_pro_content,new_pro_price):
#     sql = "UPDATE product_list SET pro_content = %s, pro_price = %s WHERE pro_name = %s;"
#     param = (new_pro_content,new_pro_price,pro_name)
#     cursor.execute(sql,param)
#     conn.commit()
#     return







# # def delete(id):
# # 	sql="delete from 表格 where 條件"
# # 	cur.execute(sql,(id,))
# # 	conn.commit()
# # 	return

# # def update(id,data):
# # 	sql="update 表格 set 欄位=值,... where 條件"
# # 	#param=('值',...)
# # 	cursor.execute(sql,param)
# # 	conn.commit()
# # 	return
