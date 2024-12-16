<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
        select {
            width: 180px;
            padding: 10px; 
            border: 1px solid #ccc; /* 加邊框 */
            border-radius: 4px; /* 邊框圓角 */
            background-color: #f9f9f9; 
            font-size: 16px; 
            cursor: pointer; /* 滑鼠移動至此顯示指針 */
            
        }

        /* 當下拉選單展開時的效果 */
        select:focus {
            border-color: #007BFF; /* 聚焦時邊框高亮 */
            outline: none; /* 去除預設的聚焦外框 */
        }
        /* 父容器使用 flexbox 排版 */
        form {
            display: flex;
            flex-direction: column; /* 每個標籤組作為一個行組 */
            max-width: 300px; /* 限制表單寬度 */
            align-items: center;
        }

        .form-group {
            display: flex; /* 讓標籤和輸入框排在同一行 */
            align-items: center; /* 垂直對齊 */
            margin-bottom: 10px; /* 每組之間的間距 */
        }

        .form-group label {
            width: 100px; /* 統一標籤寬度 */
            margin-right: 10px; /* 與輸入框的間距 */
        }

        input[type="text"], input[type="password"] {
            flex: 1; /* 讓輸入框自動填滿剩餘空間 */
            padding: 5px;
        }

        input[type="submit"] {
            margin-top: 10px; /* 與其他項目拉開間距 */
        }
    </style>
</head>
<body>
    <form id="content" method="POST" action="/login">
        <div class="form-group">
            <label for="ID">ID: </label>
            <input type="text" name="ID" id="ID" required>
        </div>
        <div class="form-group">
            <label for="PWD">Password:</label>
            <input type="password" name="PWD" id="PWD" required>
        </div>
        <div class="form-group">
            <label for="city">請選擇您的城市</label>
            <select id="options" name="options">
                <option value="台北">台北</option>
                <option value="新北">新北</option>
                <option value="桃園">桃園</option>
                <option value="新竹">新竹</option>
                <option value="基隆">基隆</option>
                <option value="台中">台中</option>
                <option value="彰化">彰化</option>
                <option value="南投">南投</option>
                <option value="雲林">雲林</option>
                <option value="嘉義">嘉義</option>
                <option value="台南">台南</option>
                <option value="高雄">高雄</option>
                <option value="屏東">屏東</option>
                <option value="台東">台東</option>
                <option value="花蓮">花蓮</option>
                <option value="宜蘭">宜蘭</option>
            </select>
        </div>
        <div class="form-group">
            <label for="car">選擇您的交通工具</label>
            <select id="options" name="options">
                <option value="機車">機車</option>
                <option value="汽車">汽車</option>
            </select>

        </div>
        <div class="form-group">
            <label for="firstName">姓氏</label>
            <input type="text" name="firstName" id="firstName" required>
        </div>
        <div class="form-group">
            <label for="lastName">名字</label>
            <input type="text" name="lastName" id="lastName" required>
        </div>
        <div class="form-group">
            <label for="phone">電話</label>
            <input type="text" name="phone" id="phone" required>
        </div>
        <div class="form-group">
            <label for="gmail">Gmail</label>
            <input type="text" name="gmail" id="gmail" required>
        </div>
        <div class="form-group">
            <label for="PID">身分證字號</label>
            <input type="text" name="PID" id="PID" required>
        </div>
        <div class="radio-group">
            <p>您是否已滿18歲</p>
            <label>
                <input type="radio" name="yes" value="yes">
                是
            </label>
            <label>
                <input type="radio" name="yes" value="yes">
                否
            </label>
        </div>


        <input type="submit" value="註冊">
    </form>
</body>
</html>
