#!/usr/local/bin/python
# Connect to MariaDB Platform
from datetime import datetime
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="rc0428",
		host="localhost",
		port=3306,
		database="FoodDelivery platform"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)

#####
#客戶註冊資料儲存至DB
def C_insertacc(acc, psw, fname, lname, tel, email, add):
	sql="insert into Client_account (ca_Acc, ca_Psw, ca_FName, ca_LName, ca_Tel, ca_Email, ca_Add) value(%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(sql, (acc, psw, fname, lname, tel, email, add))
	conn.commit()
	return

def C_gethome():
	sql="SELECT r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name;"
	cursor.execute(sql)
	return cursor.fetchall()

def C_gethome2(option):
	if (option=="1"):
		sql="SELECT r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg ASC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="2"):
		sql="SELECT r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="3"):
		sql="SELECT r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY rating ASC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="4"):
		sql="SELECT r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()