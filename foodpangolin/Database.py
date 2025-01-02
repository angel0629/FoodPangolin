import mysql.connector

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port="3306",
        database="foodpangolin"
    )
    cursor = conn.cursor(dictionary=True, buffered=True)
except mysql.connector.Error as e:
    print(e)
    print("error connecting to DB")
    exit(1)

def get_users_from_db(account, password, identity):
    if identity == '消費客戶':  # 查詢消費者資料
        sql = "SELECT * FROM customer WHERE acc = %s AND pwd = %s;"
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


# def get_restaurant_from_db(acc):
#     sql = 'SELECT * FROM restaurant WHERE acc = %s;'
#     param = (acc,)  # 加上逗號，確保這是一個元組
#     cursor.execute(sql, param)
#     user = cursor.fetchone()  # 獲取單一結果
#     return user  # 返回用戶資料


def get_customer_cart_from_sql(acc, cart_id=1):
    if cart_id:
        # 把customer跟cart找出來
        sql = "SELECT * FROM cart INNER JOIN customer ON cart.c_id = customer.c_id AND customer.acc = %s AND cart.cart_id = %s;"
        param = (acc, cart_id)  # 正確的參數順序
        cursor.execute(sql, param)
        return cursor.fetchone()  # 返回單一商品資料
    else:
        # 查詢所有商品
        sql = "SELECT * FROM cart;"
        cursor.execute(sql)
        return cursor.fetchall()  # 返回所有商品資料
    
def add_deliverer_to_db(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity):
    sql = "INSERT INTO delivery_staff(d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, d_status, identity)VALUES (%s, %s, %s, %s, %s, %s, %s, '空閒', %s)"
    param = (d_account, d_pwd, d_name, d_phone, d_city, d_car, d_gmail, identity)
    cursor.execute(sql, param)
    conn.commit()
    return

def add_customer_to_db(acc, pwd, name, telephone, email, address, identity):
    sql = "INSERT INTO customer(acc, pwd, name, telephone, email, address, identity)VALUES(%s, %s, %s, %s, %s, %s, %s)"
    param = (acc, pwd, name, telephone, email, address, identity)
    cursor.execute(sql, param)
    conn.commit()
    return
def add_restaurant_to_db(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity):
    sql = "INSERT INTO restaurant(r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)VALUES (%s, %s, %s, %s, %s, %s, %s);"
    param = (r_account, r_pwd, r_name, r_phone, r_addr, r_time, identity)
    cursor.execute(sql, param)
    conn.commit()
    return

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
	sql="""SELECT orders.o_id, customer.name,delivery_staff.d_name, orders.pickup_time, orders.delivery_time, orders.o_status,status.status_name
		FROM orders INNER JOIN customer ON orders.c_id=customer.c_id
		INNER JOIN delivery_staff ON orders.d_sid=delivery_staff.d_sid
		INNER JOIN restaurant ON orders.r_id=restaurant.r_id
        INNER JOIN status ON status.status_id=orders.o_status
		WHERE restaurant.r_id=%s
        ORDER BY o_status;
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

#外送員的部分
def get_d_id(account):
	sql="""SELECT * From delivery_staff where d_account=%s
            """

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
	sql="""SELECT * FROM orders WHERE o_status = 2;
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
    
def d_change_order_statusto3(o_id, d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `orders`
		SET `d_sid` = %s, 
			`o_status` = 3
		WHERE `o_id` = %s;
        """
        cursor.execute(sql, (d_sid ,o_id))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_change_order_statusto4(o_id, d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `orders`
		SET `d_sid` = %s, 
			`o_status` = 4
		WHERE `o_id` = %s;
        """
        cursor.execute(sql, (d_sid ,o_id))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_change_order_statusto5(o_id, d_sid): #點選上線或接單 改變外送員狀態
    try:
        sql = """
		UPDATE `orders`
		SET `d_sid` = %s, 
			`o_status` = 5
		WHERE `o_id` = %s;
        """
        cursor.execute(sql, (d_sid ,o_id))
        conn.commit()  # 提交更改
        print("Status updated successfully!")  # 確認訊息
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    

def d_find_taked_order(d_sid):
    try:
        sql = """
		SELECT * FROM `orders`
		WHERE `o_status` = 3
        AND `d_sid` = %s
        """
        cursor.execute(sql, (d_sid,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # 發生錯誤時回滾
        raise
    
def d_find_arrived_order(d_sid):
    try:
        sql = """
		SELECT * FROM `orders`
		WHERE `o_status` = 4
        AND `d_sid` = %s
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
    
    
def d_rinformation(r_id):
	sql="SELECT * FROM restaurant WHERE `r_id` = %s"
	param=(r_id,)
	cursor.execute(sql, param)
	return cursor.fetchone()

def d_cinformation(c_id):
	sql="SELECT * FROM client_account WHERE `ca_Id` = %s"
	param=(c_id,)
	cursor.execute(sql, param)
	return cursor.fetchone()

def d_getrecord(d_sid):
	sql="""
        SELECT restaurant.*
		FROM 
			orders
		INNER JOIN 
			restaurant
		ON 
			orders.r_id = restaurant.r_id
		WHERE 
			orders.o_status = 5 AND orders.d_sid = %s;
        """
	param=(d_sid,)
	cursor.execute(sql, param)
	return cursor.fetchone()

