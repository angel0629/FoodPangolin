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

#取得homepage
def C_gethome():
	sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id GROUP BY  r_name;"
	cursor.execute(sql)
	return cursor.fetchall()

#取得條件篩選排列的homepage
def C_gethome2(option, text):
	if (option=="0"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id AND restaurant.r_name LIKE %s GROUP BY  r_name;"
		cursor.execute(sql,(text,))
		return cursor.fetchall()
	if (option=="1"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id AND restaurant.r_name LIKE %s GROUP BY  r_name ORDER BY avg ASC;"
		cursor.execute(sql,(text,))
		return cursor.fetchall()
	elif (option=="2"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id AND restaurant.r_name LIKE %s GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="3"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id AND restaurant.r_name LIKE %s GROUP BY  r_name ORDER BY rating ASC;"
		cursor.execute(sql)
		return cursor.fetchall()
	elif (option=="4"):
		sql="SELECT restaurant.r_id rid, r_name name,sum(m_price) DIV COUNT(m_id) avg, (SELECT sum(rating) DIV COUNT(rating) FROM r_star WHERE r_star.r_id = restaurant.r_id LIMIT 1) rating FROM restaurant, menu WHERE restaurant.r_id = menu.r_id AND restaurant.r_name LIKE %s GROUP BY  r_name ORDER BY avg DESC;"
		cursor.execute(sql)
		return cursor.fetchall()
	
#取得各餐廳menu
def C_getmenu(Rid):
	sql="SELECT m_name name, m_price price, m_picture pic FROM menu WHERE r_id=%s;"
	cursor.execute(sql,(Rid,))
	return cursor.fetchall()

#取得各餐廳feedback
def C_getfeedback(Rid):
	sql="SELECT (SELECT ca_Fname FROM client_account WHERE r_star.ca_Id = client_account.ca_Id )user , rating, comments feedback FROM r_star WHERE r_star.r_id = %s;"
	cursor.execute(sql, (Rid,))
	return cursor.fetchall()