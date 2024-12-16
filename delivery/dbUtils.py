import mysql.connector  # mariadb 執行套件

try:
    # 連線到資料庫
    conn = mysql.connector.connect(
        user="root",  # DB預設的帳號名稱
        password="",  # DB預設的帳號密碼（空）
        host="localhost",  # 代表資料庫放在哪個電腦上
        port=3306,  # mysql預設3306 
        database="  "  # 修改為新資料庫名稱
    )
    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)


def get_user(username, password): #用戶帳號
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    return cursor.fetchone()  # 一次只獲取一行

def get_status(user_id):
    sql=
    return cursor.fetchone()

def get_order(user_id): #查看目前訂單
    query = "SELECT auction_id,item_name, item_description, starting_price FROM auctions WHERE user_id = %s"
    params = (user_id,)
    cursor.execute(query, params)
    return cursor.fetchall()  # 所有行資料一次處理

def get_cosumer():#所有拍賣紀錄
    sql = "SELECT auction_id, item_name, item_description, starting_price, COALESCE(current_high_bid, 0) as current_high_bid FROM auctions;"
    cursor.execute(sql)
    return cursor.fetchall()  




def deleteproduct(id):  #改成finish_order
    sql = "DELETE FROM auctions WHERE auction_id=%s;"
    param = (id,)
    cursor.execute(sql, param)
    conn.commit()
    return

def deleteproduct(id):  #改成finish_driven
    sql = "DELETE FROM auctions WHERE auction_id=%s;"
    param = (id,)
    cursor.execute(sql, param)
    conn.commit()
    return


def get_detail(auction_id): #改為查看訂單細項
    try:
        sql = "SELECT auction_id, item_name, item_description, starting_price, current_high_bid FROM auctions WHERE auction_id = %s"
        cursor.execute(sql, (auction_id,))
        return cursor.fetchone()  # 返回單一記錄
    except Exception as e:
        print(f"An error occurred while fetching auction details: {e}")
        raise



def get_record(aid):  #顯示送單紀錄
    try:
        sql = "SELECT bid_price, bid_time, bidder_id FROM bids WHERE auction_id = %s"
        cursor.execute(sql, (aid,))
        return cursor.fetchall()# 返回全部記錄
    except Exception as e:
        print(f"An error occurred while fetching the bids: {e}")
        raise
