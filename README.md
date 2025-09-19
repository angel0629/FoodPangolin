- 平台相關：
	- `/register`：帳號註冊頁面
	- `/register_customer`：客戶註冊頁面
	- `/register_restaurant`：餐廳註冊頁面
	- `/register_delivery`：外送人員註冊頁面
	- `/login_or_register`：登入頁面

- 客戶相關：
	- `/c_home`：客戶首頁(餐廳列表)
	- `/c_Rmenu/<餐廳名稱>/<餐廳ID>`：餐廳菜單
	- `/c_menuinfo/<餐廳名稱>/<餐廳ID>/<餐點名稱>/<餐點ID>`：餐點詳細資訊、加入購物車功能
	- `/c_car/<餐廳名稱>/<餐廳ID>`：該餐廳購物車、下單功能
	- `/c_orderlist`：已下訂清單
	- `/c_orderlistinfo/<餐廳名稱>/<訂單編號>`：訂單詳細資訊、取消&收貨功能
	- `/c_recievecheck/<餐廳名稱>/確認收貨/<訂單編號>`：確認收貨頁面
	- `/c_feedbackUPL/<餐廳名稱>/<訂單編號>`：評價輸入頁面

- 餐廳相關：
	- `/restaurant_sell_list`：餐廳訂單列表
	- `/r_more_order_info`：訂單詳細資訊
	- `/r_sell_food`：菜單列表、修改&刪除功能
	- `/r_edit_product/<餐點ID>`：餐點修改頁面
	- `/r_new`：新增餐點頁面
	

- 外送人員相關：
	- `/delivery_status`：外送人員首頁(各餐外送員狀態廳訂單列表)、切換外送員狀態功能、接單功能
	- `/order_status/<狀態ID>/delivery/<外送員ID>`：已接訂單列表、改變訂單狀態功能(抵達餐廳)
	- `/order_status/arrive/<訂單編號>/delivery/arrive/<外送員ID>`：已接訂單列表、改變訂單狀態功能(完成取餐)
	- `/order_status/finish/<訂單編號>/delivery/finish/<外送員ID>`：訂單已完成頁面、改變訂單狀態功能(完成訂單)
	- `/delivery_record/<外送員ID>`：已完成訂單紀錄列表

- 平台使用技術：
	- 	HTML
	- 	CSS
	- 	JavaScript
	-   MySQL
	-   tabase：XAMPP、MeriaDB

- 平台開發人員&分工：
	- 111213080 邱昀晴：客戶相關全端、DB建構、專案整合、readme.txt整理
	- 111213026 陳子晴：餐廳相關全端、DB建構、專案整合
	- 111213035 羅智穎：平台相關全端、DB建構、專案整合
	- 111213023 謝逸驊：外送相關全端、DB建構、專案整合
