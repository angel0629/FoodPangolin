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
		database="foodpangolin"
		#database="FoodDelivery platform"
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

#下單(client_orderlist)
def C_addorder(Rname):
	sql="INSERT INTO Client_orderlist (col_RName, col_DName, col_Num, col_DPrice, col_Sum) SELECT r_name, GROUP_CONCAT(ccl_DName SEPARATOR ', '), GROUP_CONCAT(ccl_Num SEPARATOR ', '), GROUP_CONCAT(ccl_Sum SEPARATOR ', '), sum(ccl_Sum) FROM client_carlist WHERE client_carlist.r_name=%s;"
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
	sql="SELECT GROUP_CONCAT(menu.m_id SEPARATOR ', ') AS mids FROM menu  JOIN client_carlist ON client_carlist.ccl_DName = menu.m_name AND menu.r_id = %s"
	cursor.execute(sql, (rid,))
	return cursor.fetchone()

##取得訂單statusid
def C_getstatusid(colid):
	sql="SELECT col_status status FROM client_orderlist WHERE col_Id=%s"
	cursor.execute(sql, (colid,))
	return cursor.fetchone()

##下單(orders)
def C_addoders(rid, mid, status, colid):
	sql="INSERT INTO orders (r_id, m_id, ca_Id, o_status, col_Id) value(%s, %s, %s, %s, %s)"
	cursor.execute(sql, (rid, mid, 1, status, colid,))
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

##取得按鈕功能
def C_getbtnfunc(Oid):
	sql="Delete FROM client_orderlist WHERE client_orderlist.col_Id=%s;"
	cursor.execute(sql, (Oid,))
	conn.commit()
	sql1="Delete FROM orders WHERE orders.col_Id=%s;"
	cursor.execute(sql1, (Oid,))
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