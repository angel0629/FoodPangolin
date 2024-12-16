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
def add(name,price,more,picture,my_id):
	#在自己的上架清單新增上架
	sql="INSERT INTO `menu` (`m_id`, `name`, `price`, `more`, `picture`, `r_id`) VALUES (NULL, %s, %s, %s, %s, %s);"
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
def delete(id):
	sql="DELETE FROM `menu` WHERE `menu`.`m_id` = %s;"
	cursor.execute(sql,(id,))
	conn.commit()

#更新上架商品
def update(name,price,more,picture,my_id):
	#更新自己的上架清單
	sql="UPDATE `menu` SET `name` = %s, `price` = %s, `more` = %s, `picture` = %s WHERE `menu`.`m_id` = %s"
	param=(name,price,more,picture,my_id)
	cursor.execute(sql,param)

	conn.commit()

#更改產品內容
def editList(id):
	sql="""SELECT sell.name, info, min_price, sell.s_id 
			FROM `sell` INNER JOIN users on sell.seller=users.name
			WHERE sell.s_id=%s;"""

	cursor.execute(sql,(id,))
	return cursor.fetchall()

#顯示自己上架清單
def getList(my_id):
	sql="""SELECT menu.name, menu.price, menu.picture
			FROM `menu` 
			WHERE menu.r_id=%s
            """

	cursor.execute(sql,(my_id,))
	return cursor.fetchall()

#顯示所有上架清單
def getallList():
	sql="""SELECT all_sells.s_id,sell.name,sell.info,MAX(price) AS max_price, sell.seller
			FROM `all_sells` inner join `sell` ON all_sells.s_id=sell.s_id
			GROUP BY s_id,sell.name,sell.info
            ORDER BY s_id DESC;"""
	cursor.execute(sql)
	return cursor.fetchall()

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