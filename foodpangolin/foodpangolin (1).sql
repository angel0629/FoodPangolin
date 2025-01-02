-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-01-02 04:47:04
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
-- 資料庫： `foodpangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `c_id` int(10) NOT NULL,
  `m_id` int(10) NOT NULL,
  `count` int(10) NOT NULL,
  `total_price` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `cart`
--

INSERT INTO `cart` (`cart_id`, `c_id`, `m_id`, `count`, `total_price`) VALUES
(3, 1, 3, 2, 200);

-- --------------------------------------------------------

--
-- 資料表結構 `client_account`
--

CREATE TABLE `client_account` (
  `ca_Id` int(5) UNSIGNED NOT NULL DEFAULT 1,
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

INSERT INTO `client_account` (`ca_Id`, `ca_Acc`, `ca_Psw`, `ca_FName`, `ca_LName`, `ca_Email`, `ca_Tel`, `ca_Add`) VALUES
(0, 'RC', 'RC0000', '邱', '昀晴', '99138joyce@gmail.com', '0909017161', '南投縣埔里鎮');

-- --------------------------------------------------------

--
-- 資料表結構 `client_carlist`
--

CREATE TABLE `client_carlist` (
  `r_name` varchar(15) NOT NULL DEFAULT '',
  `ca_id` int(5) UNSIGNED NOT NULL,
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
  `col_Id` varchar(6) NOT NULL,
  `col_RName` varchar(10) NOT NULL,
  `col_DName` varchar(10) NOT NULL,
  `col_DPrice` int(5) UNSIGNED NOT NULL,
  `col_Status` int(1) UNSIGNED NOT NULL,
  `col_Sum` int(5) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `c_id` int(11) NOT NULL,
  `identity` varchar(20) NOT NULL,
  `acc` varchar(50) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`c_id`, `identity`, `acc`, `pwd`, `name`, `email`, `telephone`, `address`, `birth`) VALUES
(1, '消費客戶', '123456', '456789', 'chrisluo', 'chris@gmail.com', '00000', '阿巴阿巴', '2024-12-02'),
(2, '77', '123', '456', '789', '121314', '101112', '55', NULL),
(6, '消費客戶', 'thisisacc', 'thisispwd', 'chris', 'aaaaaa@gmail.com', '0912806098', 'yilan_city', NULL),
(7, '消費客戶', 'asdf', 'sdfsd', 'chris luogasdgSsdvS', 'asdf', 'asdf', 'sdaf', NULL);

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
(8, '1', '1', '1', '1', '1', '1', '1', '1', '空閒', NULL),
(9, '外送人員', 'Chirs0888', '33535', 'Chris_luo', '0299292', 'yilan_town', '水上摩托車', '123@gmail.com', '空閒', NULL);

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
(1, 6, 1, 5, '讚讚');

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
(1, '早午餐套餐', 150, '漢堡、薯條、飲料', 'pangolin_drive-removebg-preview.png', 1, 1),
(2, 'test', 123, '主餐*2', 'pangolin_drive-removebg-preview (1).png', 1, 2),
(3, 'test', 100, '主餐*2 飲料*2 炸物*2  點心*2', '路徑', 1, 3),
(4, '龍蝦', 999, '一隻大隻的龍蝦', '路徑', 1, 4),
(5, '123', 123, '一隻大隻的龍蝦', '路徑', 1, 5),
(6, 'hi', 0, 'hi222', 'bus.jpg', 1, 7),
(8, 'test3', 333, '333', '-----------.png', 3, 8);

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
  `delivery_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`o_id`, `r_id`, `m_id`, `c_id`, `o_status`, `d_sid`, `pickup_time`, `delivery_time`) VALUES
(1, 1, 1, '1', 3, 6, NULL, NULL),
(2, 1, 2, '1', 2, 6, NULL, NULL),
(3, 1, 3, '1', 5, 7, '2025-01-23 06:55:31', NULL),
(4, 1, 4, '1', 4, 6, NULL, NULL),
(5, 3, 8, '1', 1, 7, NULL, NULL),
(6, 1, 4, '1', 2, 7, NULL, NULL);

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
(1, '餐廳業者', 'spring35', '123', '春三朝五', '台中市西屯區', '09876543277', '24營業喔'),
(2, '1', '8', '7', '6', '蔡英文', '9222', '0800'),
(3, '餐廳業者', 'asdf', 'hbh', 'chris luo', 'bjjbj', 'asdf', 'nkn');

-- --------------------------------------------------------

--
-- 資料表結構 `r_star`
--

CREATE TABLE `r_star` (
  `r_star_id` int(11) NOT NULL,
  `c_id` int(11) NOT NULL,
  `r_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `comments` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `r_star`
--

INSERT INTO `r_star` (`r_star_id`, `c_id`, `r_id`, `rating`, `comments`) VALUES
(1, 1, 1, 5, '我覺得很棒！');

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
(5, '已完成');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- 資料表索引 `client_account`
--
ALTER TABLE `client_account`
  ADD PRIMARY KEY (`ca_Id`);

--
-- 資料表索引 `client_carlist`
--
ALTER TABLE `client_carlist`
  ADD PRIMARY KEY (`r_name`);

--
-- 資料表索引 `client_orderlist`
--
ALTER TABLE `client_orderlist`
  ADD PRIMARY KEY (`col_Id`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`c_id`);

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
-- 使用資料表自動遞增(AUTO_INCREMENT) `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `c_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery_staff`
--
ALTER TABLE `delivery_staff`
  MODIFY `d_sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `d_star`
--
ALTER TABLE `d_star`
  MODIFY `d_star_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `o_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `r_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `r_star`
--
ALTER TABLE `r_star`
  MODIFY `r_star_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
