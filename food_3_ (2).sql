-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-01-06 09:25:01
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `food(3)`
--

-- --------------------------------------------------------

--
-- 資料表結構 `client_account`
--

CREATE TABLE `client_account` (
  `ca_Id` int(5) UNSIGNED NOT NULL,
  `identity` varchar(20) NOT NULL,
  `ca_Acc` varchar(20) NOT NULL,
  `ca_Psw` varchar(30) NOT NULL,
  `ca_FName` varchar(10) NOT NULL,
  `ca_LName` varchar(10) NOT NULL,
  `ca_Email` varchar(25) NOT NULL,
  `ca_Tel` varchar(10) NOT NULL DEFAULT '0',
  `ca_Add` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `client_account`
--

INSERT INTO `client_account` (`ca_Id`, `identity`, `ca_Acc`, `ca_Psw`, `ca_FName`, `ca_LName`, `ca_Email`, `ca_Tel`, `ca_Add`) VALUES
(1, '消費客戶', 'RC', 'RC0000', '邱', '昀晴', '99138joyce@gmail.com', '090901755', '南投縣埔里鎮枇杷路'),
(2, '消費客戶', '159', '951', 'oooooo', 'xxxxxxxx', 'email@gmail.com', '4444444', '台北'),
(3, '消費客戶', '123', '123', '侯', '建元', '123@gmail.com', '0988035247', '台北市'),
(4, '消費客戶', '456', '456', '寺', '武遛', '456@gmail.com', '0912335698', '台南市'),
(5, '消費客戶', '789', '789', '棲', '芭玖', '789@gmail.com', '0989889789', '屏東縣'),
(6, '消費客戶', '789', '456', '羅', '智穎', '789@gmail.com', '0912806098', 'yyt'),
(7, '消費客戶', '789', '456', '羅', '智穎', '789@gmail.com', '0912806098', 'yyt'),
(9, '消費客戶', 'customer123', '321', '羅', '志穎', 'gmail@gmail.com', '789', '全家'),
(10, '消費客戶', 'customer1', '147', '羅', 'zy=hiying', 'n  l@gmail.com', '798', '全家'),
(11, '消費客戶', '222', '222', '貳', '二二', '222@gmail.com', '0922222222', '新北市板橋區'),
(12, '消費客戶', '111', '111', '醫', '一一', '111@gmail.com', '0911111112', '台北市');

-- --------------------------------------------------------

--
-- 資料表結構 `client_carlist`
--

CREATE TABLE `client_carlist` (
  `r_name` varchar(15) NOT NULL DEFAULT '',
  `ca_Id` int(5) UNSIGNED NOT NULL,
  `ccl_DName` varchar(10) NOT NULL,
  `ccl_DPrice` int(5) UNSIGNED NOT NULL,
  `ccl_Num` int(3) UNSIGNED NOT NULL,
  `ccl_Sum` int(5) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `client_orderlist`
--

CREATE TABLE `client_orderlist` (
  `col_Id` int(11) NOT NULL,
  `col_RName` varchar(10) NOT NULL,
  `col_DName` varchar(100) NOT NULL,
  `col_DPrice` varchar(50) NOT NULL DEFAULT '',
  `col_Num` varchar(50) NOT NULL DEFAULT '',
  `col_Status` int(1) UNSIGNED NOT NULL DEFAULT 1,
  `col_Sum` int(5) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `client_orderlist`
--

INSERT INTO `client_orderlist` (`col_Id`, `col_RName`, `col_DName`, `col_DPrice`, `col_Num`, `col_Status`, `col_Sum`) VALUES
(92, '春三朝五', '測試食物', '1578', '2', 1, 1578),
(93, '春三朝五', '滿漢全席, 大龍蝦', '1578, 888', '2, 1', 1, 2466),
(94, '台北壹零壹', '自助餐', '999', '1', 1, 999);

-- --------------------------------------------------------

--
-- 資料表結構 `delivery_staff`
--

CREATE TABLE `delivery_staff` (
  `d_sid` int(11) NOT NULL,
  `identity` varchar(20) NOT NULL,
  `d_account` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `d_pwd` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `d_name` varchar(100) NOT NULL,
  `d_phone` varchar(20) NOT NULL,
  `d_city` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `d_car` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `d_gmail` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `d_status` enum('空閒','忙碌','未上線') DEFAULT '未上線',
  `d_current_order` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `delivery_staff`
--

INSERT INTO `delivery_staff` (`d_sid`, `identity`, `d_account`, `d_pwd`, `d_name`, `d_phone`, `d_city`, `d_car`, `d_gmail`, `d_status`, `d_current_order`) VALUES
(6, '外送人員', '11122', '234123', '1', '0908609225', '台北', '機車', 's111213023@gmail.com', '空閒', NULL),
(7, '', '11123', '123123', 'HSIN-HSUAN', '0908609225', '台北', '機車', '22@gmail.com', '未上線', NULL),
(8, '1', '1', '1', '我沒有明子', '0912806098', '溪班牙', '直升輝機', '讚讚@gmail.com', '未上線', NULL),
(9, '外送人員', 'Chirs0888', '33535', 'Chris_luo', '0299292', 'yilan_town', '水上摩托車', '123@gmail.com', '空閒', NULL),
(10, '外送人員', '111', '111', 'eee', '000', '高雄市', 'bubu', '111@gmail.com', '空閒', NULL),
(11, '外送人員', '222', '222', '222', '222', '南投', '腳踏車', 's111213023@gmail.com', '空閒', NULL),
(12, '外送人員', '333', '333', 'pp', '0900000000', '高雄市', '帕拉梅拉', '333@gmail.com', '空閒', NULL),
(13, '外送人員', '123', '123', 'evvvvv', '000', '高雄市', '風火輪', '123@gmail.com', '空閒', NULL),
(15, '外送人員', '190', '190', 'eee', '0900000000', '台北', '腳踏車', '111@gmail.com', '空閒', NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `d_star`
--

CREATE TABLE `d_star` (
  `d_star_id` int(11) NOT NULL,
  `d_sid` int(11) NOT NULL,
  `c_id` int(10) NOT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` between 1 and 5),
  `comments` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `d_star`
--

INSERT INTO `d_star` (`d_star_id`, `d_sid`, `c_id`, `rating`, `comments`) VALUES
(1, 8, 1, 4, '讚讚');

-- --------------------------------------------------------

--
-- 資料表結構 `menu`
--

CREATE TABLE `menu` (
  `m_id` int(11) NOT NULL,
  `m_name` varchar(15) NOT NULL,
  `m_price` int(11) NOT NULL,
  `m_detail` text NOT NULL,
  `m_picture` varchar(50) NOT NULL,
  `r_id` int(11) NOT NULL,
  `order_count` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`m_id`, `m_name`, `m_price`, `m_detail`, `m_picture`, `r_id`, `order_count`) VALUES
(1, '早午餐套餐', 150, '漢堡、薯條、飲料', 'good_deliver.png', 1, 1),
(2, '測試食物', 789, '測試', 'OIP (6).jpg', 1, 2),
(4, '滿漢全席', 789, '什麼都有www', '_5f0d4666-b4a3-4fd6-b2f8-33480bde4d7b.jpg', 1, 4),
(5, '大龍蝦', 888, '一隻大隻的龍蝦', '799.jpg', 1, 5),
(6, '讚喔', 250, '987', 'OIP (10).jpg', 1, 7),
(8, 'test3', 333, '333', '-----------.png', 3, 8),
(9, '仙人掌', 200, '蛤', '螢幕擷取畫面 2025-01-02 032700.png', 1, 0),
(10, '蔡英文', 799, '很蔡', 'OIP (4).jpg', 1, 0),
(11, '賴清德', 899, '很賴', 'OIP (5).jpg', 1, 0),
(12, '人間美味', 159, 'hi', 'OIP (9).jpg', 1, 0),
(13, '讚喔', 120, '還是很讚', 'd3671056.jpg', 1, 0),
(14, '自助餐', 999, '整間自助餐吃到飽，限時3小時', 'default.jpg', 4, 0),
(16, '自助餐', 999, '在101上吃自助餐', 'default.jpg', 5, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `o_id` int(11) NOT NULL,
  `r_id` int(20) NOT NULL,
  `m_id` int(10) NOT NULL,
  `c_id` varchar(100) NOT NULL,
  `o_status` int(11) DEFAULT NULL,
  `d_sid` int(11) DEFAULT NULL,
  `pickup_time` datetime DEFAULT NULL,
  `delivery_time` datetime DEFAULT NULL,
  `col_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`o_id`, `r_id`, `m_id`, `c_id`, `o_status`, `d_sid`, `pickup_time`, `delivery_time`, `col_Id`) VALUES
(78, 1, 2, '1', 6, 15, '2025-01-05 20:11:29', '2025-01-05 20:11:44', 92),
(79, 1, 4, '1', 5, 15, '2025-01-05 20:16:58', '2025-01-05 20:17:03', 93),
(80, 5, 16, '1', 1, NULL, NULL, NULL, 94);

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `r_id` int(11) NOT NULL,
  `identity` varchar(20) NOT NULL,
  `r_account` varchar(20) NOT NULL,
  `r_pwd` varchar(15) NOT NULL,
  `r_name` varchar(15) NOT NULL,
  `r_addr` text NOT NULL,
  `r_phone` varchar(15) NOT NULL,
  `r_time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`r_id`, `identity`, `r_account`, `r_pwd`, `r_name`, `r_addr`, `r_phone`, `r_time`) VALUES
(1, '餐廳業者', 'spring35', '123', '春三朝五', '台中市西屯區', '09876543277', '24營業'),
(5, '餐廳業者', 'taipei101', '101', '台北壹零壹', '台北市信義區', '0987654321', '一~五 12:00~20:00 六、日公休'),
(6, '餐廳業者', 'happy', '123', '開心', '台北市信義區', '0987654321', '24小時營業');

-- --------------------------------------------------------

--
-- 資料表結構 `r_star`
--

CREATE TABLE `r_star` (
  `r_star_id` int(11) NOT NULL,
  `c_id` int(11) NOT NULL,
  `r_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `comments` text NOT NULL,
  `ca_Id` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `r_star`
--

INSERT INTO `r_star` (`r_star_id`, `c_id`, `r_id`, `rating`, `comments`, `ca_Id`) VALUES
(20, 12, 1, 4, '好吃', 12);

-- --------------------------------------------------------

--
-- 資料表結構 `status`
--

CREATE TABLE `status` (
  `status_id` int(11) NOT NULL,
  `status_name` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 傾印資料表的資料 `status`
--

INSERT INTO `status` (`status_id`, `status_name`) VALUES
(1, '待餐廳接單'),
(2, '待外送員接單'),
(3, '待外送員取餐'),
(4, '配送中'),
(5, '已完成'),
(6, '隱藏');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `client_account`
--
ALTER TABLE `client_account`
  ADD PRIMARY KEY (`ca_Id`);

--
-- 資料表索引 `client_orderlist`
--
ALTER TABLE `client_orderlist`
  ADD PRIMARY KEY (`col_Id`);

--
-- 資料表索引 `delivery_staff`
--
ALTER TABLE `delivery_staff`
  ADD PRIMARY KEY (`d_sid`),
  ADD UNIQUE KEY `unique_d_account` (`d_account`),
  ADD KEY `fk_current_order` (`d_current_order`);

--
-- 資料表索引 `d_star`
--
ALTER TABLE `d_star`
  ADD PRIMARY KEY (`d_star_id`),
  ADD KEY `fk_delivery_staff` (`d_sid`);

--
-- 資料表索引 `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`m_id`);

--
-- 資料表索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`o_id`);

--
-- 資料表索引 `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`r_id`);

--
-- 資料表索引 `r_star`
--
ALTER TABLE `r_star`
  ADD PRIMARY KEY (`r_star_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `client_account`
--
ALTER TABLE `client_account`
  MODIFY `ca_Id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `client_orderlist`
--
ALTER TABLE `client_orderlist`
  MODIFY `col_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery_staff`
--
ALTER TABLE `delivery_staff`
  MODIFY `d_sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `d_star`
--
ALTER TABLE `d_star`
  MODIFY `d_star_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `o_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `r_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `r_star`
--
ALTER TABLE `r_star`
  MODIFY `r_star_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `delivery_staff`
--
ALTER TABLE `delivery_staff`
  ADD CONSTRAINT `fk_current_order` FOREIGN KEY (`d_current_order`) REFERENCES `orders` (`o_id`) ON DELETE SET NULL;

--
-- 資料表的限制式 `d_star`
--
ALTER TABLE `d_star`
  ADD CONSTRAINT `fk_delivery_staff` FOREIGN KEY (`d_sid`) REFERENCES `delivery_staff` (`d_sid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
