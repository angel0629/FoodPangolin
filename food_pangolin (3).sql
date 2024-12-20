-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-20 10:07:44
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
-- 資料庫： `food_pangolin`
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
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `c_id` int(11) NOT NULL,
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

INSERT INTO `customer` (`c_id`, `acc`, `pwd`, `name`, `email`, `telephone`, `address`, `birth`) VALUES
(1, '123456', '456789', 'chrisluo', 'chris@gmail.com', '00000', '阿巴阿巴', '2024-12-02');

-- --------------------------------------------------------

--
-- 資料表結構 `delivery_staff`
--

CREATE TABLE `delivery_staff` (
  `d_sid` int(11) NOT NULL,
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

INSERT INTO `delivery_staff` (`d_sid`, `d_account`, `d_pwd`, `d_name`, `d_phone`, `d_city`, `d_car`, `d_gmail`, `d_status`, `d_current_order`) VALUES
(6, '11122', '234123', '1', '0908609225', '台北', '機車', 's111213023@gmail.com', '空閒', NULL),
(7, '11123', '123123', 'HSIN-HSUAN', '0908609225', '台北', '機車', '22@gmail.com', '未上線', NULL);

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
  `m_picture` text NOT NULL,
  `r_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`m_id`, `m_name`, `m_price`, `m_detail`, `m_picture`, `r_id`) VALUES
(1, '早午餐套餐', 150, '漢堡、薯條、飲料', '應該會是存網址或圖片路徑(?', 1),
(2, 'test', 123, '主餐*2 飲料*2 炸物*2  點心*2', '路徑', 1),
(3, 'test', 100, '主餐*2 飲料*2 炸物*2  點心*2', '路徑', 1),
(4, '龍蝦', 999, '一隻大隻的龍蝦', '路徑', 1),
(5, '123', 123, '一隻大隻的龍蝦', '路徑', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `o_id` int(11) NOT NULL,
  `c_id` varchar(100) NOT NULL,
  `o_status` enum('待接單','已接單','配送中','已完成') DEFAULT '待接單',
  `d_sid` int(11) DEFAULT NULL,
  `pickup_time` datetime DEFAULT NULL,
  `delivery_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`o_id`, `c_id`, `o_status`, `d_sid`, `pickup_time`, `delivery_time`) VALUES
(1, '12', '待接單', 6, NULL, NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `r_id` int(11) NOT NULL,
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

INSERT INTO `restaurant` (`r_id`, `r_account`, `r_pwd`, `r_name`, `r_addr`, `r_phone`, `r_time`) VALUES
(1, 'spring35', '123', '春三朝五', '台中市西屯區', '0987654321', '24營業');

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

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

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
  MODIFY `c_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery_staff`
--
ALTER TABLE `delivery_staff`
  MODIFY `d_sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `d_star`
--
ALTER TABLE `d_star`
  MODIFY `d_star_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `m_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `o_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `r_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
