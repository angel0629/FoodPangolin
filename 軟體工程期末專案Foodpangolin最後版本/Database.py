import mysql.connector
from datetime import datetime

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port="3306",
        database="food(3)"
    )
    cursor = conn.cursor(dictionary=True, buffered=True)
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
    # 把client_account的user資料找出來
    sql = "SELECT * FROM client_account where client_account.ca_Acc = %s;"
    param = (acc,) 
    cursor.execute(sql, param)
    return cursor.fetchone()  

    
    
def add_deliverer_to_db(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity):
    sql = "INSERT INTO delivery_staff(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, d_status, identity)VALUES (%s, %s, %s, %s, %s, %s, %s, '未上線', %s)"
    param = (d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity)
    cursor.execute(sql, param)
    conn.commit()
    return


def add_customer_to_db(acc, pwd, fname, lname, telephone, email, address):
    sql = """
    INSERT INTO Client_account(ca_Acc, ca_Psw, ca_FName, ca_LName, ca_Tel, ca_Email, ca_Add, identity)
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
    sql = "SELECT sum(client_orderlist.col_Sum) as total_revenue FROM orders INNER JOIN client_orderlist ON orders.col_Id=client_orderlist.col_Id WHERE r_id=%s and orders.o_status >=2;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出該餐廳有多少餐點被下訂 chrisluo
def find_today_total_orders(r_id):
    sql = "SELECT COUNT(o_id) AS total_orders FROM `orders` WHERE r_id = %s and orders.o_status >=2;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出status=6，已完成訂單 chrisluo
def find_finished_order(r_id):
    sql = "SELECT COUNT(orders.o_status) AS completed_orders FROM orders INNER JOIN status ON orders.o_status = status.status_id WHERE orders.r_id = %s AND status.status_id >=5;"
    param = (r_id,)  
    cursor.execute(sql, param)
    result = cursor.fetchone()  
    return result
#找出明星商品跟銷售數量chrisluo
def find_bestsell_and_num(r_id):
    sql = "SELECT col_DName, col_Num FROM `client_orderlist` INNER JOIN orders on orders.col_Id = client_orderlist.col_Id INNER JOIN restaurant ON restaurant.r_id = orders.r_id WHERE orders.r_id = %s;"
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

#抓出turnover資料chrisluo，改成狀態>=5
def find_r_turnover(r_id):
    sql='SELECT orders.o_id, orders.pickup_time, menu.m_detail, menu.m_price, menu.m_id AS menu_item_id,status.status_name FROM orders INNER JOIN menu ON orders.m_id = menu.m_id INNER JOIN status ON orders.o_status = status.status_id WHERE orders.r_id = %s AND status.status_id >= 5 ORDER BY orders.pickup_time DESC, orders.o_id ASC;'
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

def r_get_r_name(id):
	sql="""SELECT * FROM restaurant WHERE r_id=%s"""

	cursor.execute(sql,(id,))
	return cursor.fetchone()


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
	sql="""SELECT orders.o_id, client_account.ca_FName,delivery_staff.d_name, orders.pickup_time, orders.delivery_time, orders.o_status, status.status_name,client_orderlist.col_Num,client_orderlist.col_Id, client_orderlist.col_Sum
		FROM orders INNER JOIN client_account ON orders.c_id=client_account.ca_Id
		LEFT JOIN delivery_staff ON orders.d_sid=delivery_staff.d_sid
		INNER JOIN restaurant ON orders.r_id=restaurant.r_id
		INNER JOIN status ON status.status_id = orders.o_status
		INNER JOIN client_orderlist ON client_orderlist.col_Id = orders.col_Id
		WHERE restaurant.r_id=%s
		ORDER BY orders.o_status;
		"""
	cursor.execute(sql,(my_id,))
	return cursor.fetchall()

def r_acceptList(o_id):
	sql="UPDATE `orders` SET `o_status` = %s WHERE `orders`.`o_id` = %s"
	param=(2,o_id)
	cursor.execute(sql,param)
	conn.commit()

def r_announced_deliver(o_id):
	sql="UPDATE `orders` SET `o_status` = %s WHERE `orders`.`o_id` = %s"
	param=(4,o_id)
	cursor.execute(sql,param)
	conn.commit()
def get_r_id(account):
	sql="""SELECT restaurant.r_id From restaurant where r_account=%s
            """

	cursor.execute(sql,(account,))
	return cursor.fetchone()      

#取得訂單詳細內容
def r_getorderinfo(col_id):
	sql="""
	SELECT col_RName Rname, col_DName Dname, col_DPrice Dprice, col_Num num, col_Sum sum 
	FROM client_orderlist 
	WHERE client_orderlist.col_Id=%s
	"""
	cursor.execute(sql, (col_id,))
	return cursor.fetchall()

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

##取得姓氏
def C_getfname(my_id):
	sql="SELECT ca_FName fname FROM client_account WHERE ca_Id=%s;"
	cursor.execute(sql, (my_id, ))
	return cursor.fetchone()

#取得homepage
def C_gethome():
	sql="""SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
	(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
	FROM restaurant, menu 
	WHERE restaurant.r_id = menu.r_id 
	GROUP BY  rid;
	"""
	cursor.execute(sql)
	return cursor.fetchall()

#取得條件篩選排列的homepage
def C_gethome2(option, text):
	if (text != ""):
		sql="""
		SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
		(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
		FROM restaurant, menu 
		WHERE restaurant.r_id = menu.r_id  
		AND restaurant.r_name LIKE %s;
		"""
		cursor.execute(sql,(text,))
		return cursor.fetchall()

	if (option=="1"):
		sql="""
		SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
		(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
		FROM restaurant, menu 
		WHERE restaurant.r_id = menu.r_id 
		GROUP BY  r_name 
		ORDER BY avg ASC;
		"""
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="2"):
		sql="""
		SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
		(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
		FROM restaurant, menu 
		WHERE restaurant.r_id = menu.r_id 
		GROUP BY  r_name 
		ORDER BY avg DESC;
		"""
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="3"):
		sql="""
		SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
		(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
		FROM restaurant, menu 
		WHERE restaurant.r_id = menu.r_id
		GROUP BY  r_name 
		ORDER BY rating ASC;
		"""
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="4"):
		sql="""
		SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, 
		(SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating 
		FROM restaurant, menu 
		WHERE restaurant.r_id = menu.r_id 
		GROUP BY  r_name 
		ORDER BY avg DESC;
		"""
		cursor.execute(sql)
		return cursor.fetchall()

#取得各餐廳menu
def C_getmenu(Rid):
	sql="SELECT m_id mid, m_name name, m_price price, m_picture pic FROM menu WHERE r_id=%s;"
	cursor.execute(sql,(Rid,))
	return cursor.fetchall()

#取得各餐廳feedback
def C_getfeedback(Rid):
	sql="""
	SELECT (SELECT ca_Fname FROM client_account WHERE r_star.ca_Id = client_account.ca_Id )user , rating, comments feedback 
	FROM r_star WHERE r_star.r_id = %s;
	"""
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
	cursor.execute(sql, (Rname, 1, Dname, Dprice, Num, Sum))
	conn.commit()

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

#下單(client_orderlist)
def C_addorder(Rname):
	sql="""
	INSERT INTO Client_orderlist (col_RName, col_DName, col_Num, col_DPrice, col_Sum) 
	SELECT r_name, GROUP_CONCAT(ccl_DName SEPARATOR ', '), GROUP_CONCAT(ccl_Num SEPARATOR ', '), GROUP_CONCAT(ccl_Sum SEPARATOR ', '), sum(ccl_Sum) 
	FROM client_carlist 
	WHERE client_carlist.r_name=%s;
	"""
	cursor.execute(sql, (Rname,))
	conn.commit()
	sql1="Delete FROM client_carlist WHERE r_name=%s;"
	cursor.execute(sql1, (Rname,))
	conn.commit()
	return

##取得訂單colid
def C_getcolid():
	sql="SELECT LAST_INSERT_ID() AS colid;"
	cursor.execute(sql)
	return cursor.fetchone()

##取得下單餐點mid
def C_getmid(rid):
	sql="""
	SELECT GROUP_CONCAT(menu.m_id SEPARATOR ', ') AS mids 
	FROM menu  
	JOIN client_carlist 
	ON client_carlist.ccl_DName = menu.m_name 
	AND menu.r_id = %s
	"""
	cursor.execute(sql, (rid,))
	return cursor.fetchone()

##取得訂單statusid
def C_getstatusid(colid):
	sql="SELECT col_status status FROM client_orderlist WHERE col_Id=%s"
	cursor.execute(sql, (colid,))
	return cursor.fetchone()

##下單(orders)
def C_addoders(rid, mid, status, colid):
	sql="INSERT INTO orders (r_id, m_id, c_id, o_status, col_Id) value(%s, %s, %s, %s, %s)"
	cursor.execute(sql, (rid, mid, 1, status, colid,))
	conn.commit()
	return

# #取得訂單列表
# def C_getorderlist():
# 	sql="SELECT col_Id Oid, col_RName Rname, col_Sum sum FROM client_orderlist;"
# 	cursor.execute(sql)
# 	return cursor.fetchall()

#取得訂單列表
def C_getorderlist():
	sql="""
	SELECT client_orderlist.col_Id Oid, col_RName Rname, col_Sum sum FROM client_orderlist
	JOIN orders
	ON client_orderlist.col_Id=orders.col_Id
	AND orders.o_status < 6
	"""
	cursor.execute(sql)
	return cursor.fetchall()

#取得訂單詳細內容
def C_getorderinfo(Rname, Oid):
	sql="""
	SELECT col_RName Rname, col_DName Dname, col_DPrice Dprice, col_Num num, col_Sum sum, orders.o_status status 
	FROM client_orderlist 
	INNER JOIN orders 
	ON client_orderlist.col_Id=orders.col_Id 
	WHERE client_orderlist.col_RName=%s 
	AND client_orderlist.col_Id=%s
	"""
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

##取得按鈕功能：取消訂單
def C_getbtnfunc1(Oid):
	sql="Delete FROM client_orderlist WHERE client_orderlist.col_Id=%s;"
	cursor.execute(sql, (Oid,))
	conn.commit()
	return

##取得按鈕功能：確認收貨
def C_getbtnfunc2(Oid): 
	sql="UPDATE orders SET o_status = 6 WHERE orders.col_Id=%s;"
	cursor.execute(sql, (Oid,))
	conn.commit()
	return

#取得rid
def C_getrid(Rname):
	sql="SELECT r_id rid FROM restaurant WHERE restaurant.r_name=%s"
	cursor.execute(sql, (Rname,))
	return cursor.fetchone()

#新增評論至DB
def C_insertfb(myid, rid, rating, comment):
	sql="INSERT INTO r_star (c_id, r_id, rating, comments, ca_Id) VALUE(%s, %s, %s, %s, %s);"
	cursor.execute(sql, (myid, rid, rating, comment, myid,))
	conn.commit()
	return 

#-----------------------------------------------------




#外送員的部分
def get_d_id(account):
	sql="""SELECT * From delivery_staff where d_account=%s"""
	cursor.execute(sql,(account,))
	return cursor.fetchone() 

def get_delivery_staff(d_sid):  # 取得外送員資訊
    sql = "SELECT * FROM delivery_staff WHERE d_sid = %s"
    cursor.execute(sql, (d_sid,))  # 注意這裡加上逗號，確保是 tuple
    result = cursor.fetchone()
    if result:
        return result
    return None

def d_get_orderlist(): #查看目前訂單
	sql="""
    SELECT 
    restaurant.r_name , orders.* ,cl.col_Sum
    FROM orders
    INNER JOIN restaurant
    ON orders.r_id = restaurant.r_id 
	INNER JOIN client_orderlist cl ON 	
    orders.col_Id = cl.col_Id WHERE orders.o_status=2;
    """
	cursor.execute(sql)
	return cursor.fetchall()


def d_status(d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
        UPDATE `delivery_staff`
		SET `d_status` = '空閒'
		WHERE `d_sid` = %s;

        """
        cursor.execute(sql, (d_sid,))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise	
    
def d_status_out(d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
        UPDATE `delivery_staff`
		SET `d_status` = '未上線'
		WHERE `d_sid` = %s;

        """
        cursor.execute(sql, (d_sid,))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise

def d_change_staff_status(d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `delivery_staff`
		SET `d_status` = '忙碌'
		WHERE `d_sid` = %s;
        """
        cursor.execute(sql, (d_sid,))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_change_staff_status2(d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `delivery_staff`
		SET `d_status` = '空閒'
		WHERE `d_sid` = %s;
        """
        cursor.execute(sql, (d_sid,))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_change_order_statusto3(o_id, d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `orders`
		SET `d_sid` = %s, 
			`o_status` = 3
		WHERE `o_id` = %s AND `o_status` NOT IN (4, 5) AND (
			`d_sid` IS NULL OR `d_sid` = %s
		);
        """
        cursor.execute(sql, (d_sid, o_id, d_sid,))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise

def get_order_status(o_id):
    try:
        sql = "SELECT o_status FROM orders WHERE o_id = %s"
        cursor.execute(sql, (o_id,))
        result = cursor.fetchone()
        if result:
            return result["o_status"]
        else:
            return None  # 訂單不存在
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise

# def d_change_order_statusto4(o_id, d_sid): #點選上線或接單 改變外送員狀態
#     try:
#         sql = """
# 		UPDATE `orders`
# 		SET `o_status` = 4
# 		WHERE `o_id` = %s;
#         """
#         cursor.execute(sql, (d_sid ,o_id,))
#         conn.commit()  # 提交更改
#         print("Status updated successfully!")  # 確認訊息
#     except mysql.connector.Error as err:
#         print(f"Database error: {err}")
#         conn.rollback()  # 發生錯誤時回滾
#         raise
    
def d_change_order_statusto5(o_id): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `orders`
		SET `o_status` = 5, `delivery_time` = now()
		WHERE `o_id` = %s;
        """
        cursor.execute(sql, (o_id,))
        conn.commit()  # 提交更改
        # cursor.fetchall()  # 清空結果集
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_find_taked_order(d_sid):
    try:
        sql = """
		SELECT * FROM `orders` WHERE (`o_status` = 3 
            OR `o_status` = 4 ) AND `d_sid` = %s;
        """
        cursor.execute(sql, (d_sid,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise

def d_find_finished_order(d_sid):
    try:
        sql = """
		SELECT * FROM `orders`
		WHERE `o_status` = 5
        AND `d_sid` = %s
        """
        cursor.execute(sql, (d_sid,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
    
def d_rinformation(r_id): #找餐廳ID
	sql="SELECT * FROM restaurant WHERE `r_id` = %s"
	param=(r_id,)
	cursor.execute(sql, param)
	return cursor.fetchone()

def d_cinformation(c_id):   #找客戶id
	sql="SELECT * FROM client_account WHERE `ca_Id` = %s"
	param=(c_id,)
	cursor.execute(sql, param)
	return cursor.fetchone()

def d_getrecord(d_sid):
	sql="""
        SELECT restaurant.* ,cl.col_Sum
		FROM 
			orders
		INNER JOIN 
			restaurant
		ON 
			orders.r_id = restaurant.r_id
		LEFT JOIN client_orderlist cl ON 	
    	orders.col_Id = cl.col_Id 
		WHERE 
			orders.o_status = 5 AND orders.d_sid = %s;
        """
	param=(d_sid,)
	cursor.execute(sql, param)
	return cursor.fetchall()


def d_get_order_status(d_sid):
    query = "SELECT * FROM orders WHERE d_sid = %s and (o_status = 3 or o_status = 4);"
    cursor.execute(query, (d_sid,))
    result = cursor.fetchone()
    return result

#chrisluo新增delivery_home
def get_dsid(account):
	sql="SELECT d_sid From delivery_staff where d_account=%s"
	cursor.execute(sql,(account,))
	return cursor.fetchone() 

def total_order_info(d_sid):
    query = "SELECT SUM(client_orderlist.col_Sum * 0.15) as total_revenue FROM orders left JOIN client_orderlist ON client_orderlist.col_Id = orders.col_Id WHERE orders.d_sid = %s;"
    cursor.execute(query, (d_sid,))
    result = cursor.fetchall()
    return result

def order_info(d_sid):
    query = "SELECT orders.o_id,orders.delivery_time,restaurant.r_name,restaurant.r_addr,(client_orderlist.col_Sum * 0.15) AS income FROM orders INNER JOIN restaurant ON orders.r_id = restaurant.r_id left JOIN client_orderlist ON client_orderlist.col_Id = orders.col_Id WHERE orders.d_sid = %s;"
    cursor.execute(query, (d_sid,))
    result = cursor.fetchall()
    return result

def count_delivery_goodrate(d_sid):
    query = "SELECT d_star.c_id,SUM(CASE WHEN d_star.rating >= 4 THEN 1 ELSE 0 END) AS GOOD_TIMES, (SUM(CASE WHEN d_star.rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS good_review_rate, d_star.d_sid, d_star.comments, d_star.rating FROM d_star INNER JOIN delivery_staff ON d_star.d_sid = delivery_staff.d_sid WHERE d_star.d_sid = %s;"
    cursor.execute(query, (d_sid,))
    result = cursor.fetchall()
    return result

def find_d_information(d_sid):
    sql='SELECT * FROM `delivery_staff` WHERE d_sid=%s;'
    param = (d_sid,)  
    cursor.execute(sql, param)
    result = cursor.fetchall()  
    return result

def update_delivery_info(dname, dphone, dcity,dcar,dgmail,d_sid):
    sql='UPDATE delivery_staff SET d_name = %s, d_phone = %s, d_city = %s,d_car=%s,d_gmail=%s WHERE d_sid = %s'
    param = (dname, dphone, dcity,dcar,dgmail,d_sid,)  
    cursor.execute(sql, param)
    conn.commit()
    
def update_customer_info(caFName,caLname,caEmail,caTel,caAdd,ca_Id):
    sql = 'UPDATE client_account SET ca_FName = %s, ca_LName = %s, ca_Email = %s,ca_Tel=%s,ca_Add=%s WHERE ca_Id = %s;'
    param = (caFName,caLname,caEmail,caTel,caAdd,ca_Id,)  
    cursor.execute(sql, param)
    conn.commit()

def get_customer_info(acc):
    sql = "SELECT * FROM client_account where client_account.ca_Id = %s;"
    param = (acc,)  
    cursor.execute(sql, param)
    return cursor.fetchone()   

      
def get_ca_id(account):
    sql="SELECT client_account.ca_Id From client_account where ca_Acc=%s"
    cursor.execute(sql,(account,))
    return cursor.fetchone()


def get_pickup_time(pickup_time, d_sid, o_id):
    pickup_time = datetime.now()
    sql = """UPDATE orders SET pickup_time = %s WHERE d_sid = %s AND o_id = %s"""
    cursor.execute(sql, (pickup_time, d_sid, o_id,))
    conn.commit()


def get_delivery_time(delivery_time,d_sid, o_id):
    delivery_time = datetime.now()  # 獲取當前時間
    sql = """UPDATE orders SET delivery_time = %s WHERE d_sid = %s AND o_id = %s"""
    cursor.execute(sql, (delivery_time, d_sid, o_id,))
    conn.commit()


# def add_product_to_sql(pro_name,pro_content,pro_price):
#     # 資料庫語句，後面的值也是資料庫中項目的名子
#     sql="insert into product_list (pro_name,pro_content,pro_price) VALUES (%s,%s,%s) " 
#     param=(pro_name,pro_content,pro_price)
#     cursor.execute(sql,param)
#     conn.commit()
#     return

    
# def d_find_arrived_order(d_sid):
#     try:
#         sql = """
# 		SELECT * FROM `orders`
# 		WHERE `o_status` = 4
#         AND `d_sid` = %s
#         """
#         cursor.execute(sql, (d_sid,))
#         return cursor.fetchone()
#     except mysql.connector.Error as err:
#         print(f"Database error: {err}")
#         conn.rollback()  # 發生錯誤時回滾
#         raise




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
