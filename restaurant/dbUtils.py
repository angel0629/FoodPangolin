#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb
from flask import Flask, render_template, request, session, redirect

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="food_pangolin"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)


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
			database="food_pangolin"
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


'''
#顯示細節
def details(id):
	sql="""SELECT all_sells.s_id,sell.name,sell.info,price, all_sells.u_id AS username
	FROM `all_sells` inner join `sell` ON all_sells.s_id=sell.s_id 
	WHERE all_sells.s_id=%s ORDER BY price DESC;"""
	cursor.execute(sql,(id,))
	return cursor.fetchall()

#給購買頁面現在要購買商品之最大值
def buy(id):
	sql="""SELECT all_sells.s_id,sell.name,sell.info,MAX(price) AS max_price 
			FROM `all_sells` inner join `sell` ON all_sells.s_id=sell.s_id
            WHERE all_sells.s_id=%s
			GROUP BY s_id,sell.name,sell.info;"""
	cursor.execute(sql,(id,))
	return cursor.fetchall()

#確定可以購買後的新增頁面
def new_buy(id, new_price,my_id):
	sql="INSERT INTO `all_sells` (`id`, `s_id`, `price`, `u_id`) VALUES (NULL, %s, %s, %s)"
	param=(id,new_price,my_id)
	cursor.execute(sql,param)
	conn.commit()

#顯示購物清單
def get_shop(id):
	sql="""SELECT all_sells.s_id,sell.name,sell.info,MAX(price) AS max_price 
			FROM `all_sells` inner join `sell` ON all_sells.s_id=sell.s_id
            WHERE all_sells.u_id=%s
			GROUP BY s_id,sell.name,sell.info
            ORDER BY s_id DESC;"""
	cursor.execute(sql,(id,))
	return cursor.fetchall()
'''
