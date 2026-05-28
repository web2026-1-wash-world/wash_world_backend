-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: May 27, 2026 at 11:58 AM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2026_1_wash_world`
--

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `car_pk` char(32) NOT NULL,
  `user_id` char(32) NOT NULL,
  `car_license_plate` varchar(7) NOT NULL,
  `car_brand` varchar(20) NOT NULL,
  `car_model` varchar(65) DEFAULT NULL,
  `car_created_at` bigint(20) UNSIGNED NOT NULL,
  `car_updated_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`car_pk`, `user_id`, `car_license_plate`, `car_brand`, `car_model`, `car_created_at`, `car_updated_at`) VALUES
('0eef122ed4c748a188753a0b86446885', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798952, 1779798952),
('2db77e1d65574b8a8e11b2d2540f7adf', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798926, 1779798926),
('31a012ac6d2a4b0595332c6e50d4de70', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798585, 1779798585),
('44ba765b6fae4900931664af345709b1', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'a', 'BB', 1779798677, 1779798677),
('45e77dfe77f849178451c1dc5b15d049', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798587, 1779798587),
('5d12b8f2e2b14279aec29c001dafb37a', '5d318c0ef62e4742ae373cf5269b65a9', 'AB12342', 'aaaaaa', 'Bbbbbbb', 1779800612, 1779800612),
('62f55a43ea1b46249ce30d55881a4abd', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798404, 1779798404),
('a130ca96a7cb4da0a2075d8ced3833b4', '5d318c0ef62e4742ae373cf5269b65a9', 'AB12342', 'aaaaaa', 'Bbbbbbb', 1779799442, 1779799442),
('a53945f0f49c4d7c90459d607909e302', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'AA', 'BB', 1779798316, 1779798316),
('e62f57d7a53c43838059f227bc289f5a', 'de2faaff78fb46f2b7fdb4f316b59e1f', 'AB12345', 'A', 'BB', 1779798664, 1779798664);

-- --------------------------------------------------------

--
-- Table structure for table `memberships`
--

CREATE TABLE `memberships` (
  `membership_pk` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `price_per_month` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `memberships`
--

INSERT INTO `memberships` (`membership_pk`, `name`, `price_per_month`) VALUES
(1, 'Guld', 139),
(2, 'Premium', 169),
(3, 'Brilliant', 199);

-- --------------------------------------------------------

--
-- Table structure for table `stations`
--

CREATE TABLE `stations` (
  `station_pk` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `adress` varchar(150) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stations`
--

INSERT INTO `stations` (`station_pk`, `name`, `adress`, `latitude`, `longitude`) VALUES
(1, 'Wash World Aabenraa Egevej', 'Egevej 4, 6200 Aabenraa', 55.065643, 9.364450),
(2, 'Wash World Aalborg Otto Mønstedsvej', 'Otto Mønsteds Vej 5, 9200 Aalborg', 57.015248, 9.896256),
(3, 'Wash World Aalborg Gug Gammel Vissevej', 'Gammel Vissevej 1C, 9210 Aalborg - Gug', 57.006314, 9.925946),
(4, 'Wash World Ballerup Industriparken', 'Industriparken 6, 2750 Ballerup', 55.728714, 12.373295),
(5, 'Wash World Brande Vestergårdsvej', 'Vestergårdsvej 3, 7330 Brande', 55.960647, 9.103426),
(6, 'Wash World Brøndby Strand Gl. Køge Landevej', 'Gammel Køge Landevej 690, 2660 Brøndby Strand', 55.618231, 12.423950),
(7, 'Wash World Ebeltoft Færgevejen', 'Færgevejen 3, 8400 Ebeltoft', 56.190809, 10.672123),
(8, 'Wash World Esbjerg Sædding Ringvej', 'Sædding Ringvej 6, 6710 Esbjerg', 55.503728, 8.407419),
(9, 'Wash World Farum Gammelgårdsvej', 'Gammelgårdsvej 84, 3520 Farum', 55.816943, 12.370350),
(10, 'Wash World Fredericia Strevelinsvej', 'Strevelinsvej 5, 7000 Fredericia', 55.535519, 9.718700),
(11, 'Wash World Fredericia Vejlevej', 'Vejlevej 20, 7000 Fredericia', 55.569691, 9.727622),
(12, 'Wash World Frederikshavn Apholmenvej', 'Apholmenvej 9, 9900 Frederikshavn', 57.462193, 10.519448),
(13, 'Wash World Frederikssund Askelundsvej', 'Askelundsvej 8, 3600 Frederikssund', 55.845151, 12.074291),
(14, 'Wash World Frederiksværk Hanehovedvej', 'Hanehovedvej 49, 3300 Frederiksværk', 55.977559, 12.007447),
(15, 'Wash World Grenå Hesselvang', 'Hesselvang 1, 8500 Grenå', 56.383895, 10.864451),
(16, 'Wash World Haderslev Sverigesvej', 'Sverigesvej 2M, 6100 Haderslev', 55.259211, 9.474129),
(17, 'Wash World Helsingør Klostermosevej', 'Klostermosevej 103, 3000 Helsingør', 56.024018, 12.571863),
(18, 'Wash World Herlev Nørrelundvej', 'Nørrelundvej 2, 2730 Herlev', 55.725365, 12.416697),
(19, 'Wash World Herning Dæmningen', 'Dæmningen 21, 7400 Herning', 56.132141, 8.959350),
(20, 'Wash World Herning Guldborgvej', 'Guldborgvej 2-4, 7400 Herning', 56.153554, 8.984745),
(21, 'Wash World Hillerød Industrivænget', 'Industrivænget 3, 3400 Hillerød', 55.931481, 12.282996),
(22, 'Wash World Hjørring Sprogøvej', 'Sprogøvej 2, 9800 Hjørring', 57.455594, 10.039465),
(23, 'Wash World Holbæk Springstrup', 'Springstrup 5, 4300 Holbæk', 55.703026, 11.666091),
(24, 'Wash World Holstebro Nybo Bakke', 'Nybo Bakke 2, 7500 Holstebro', 56.341889, 8.635395),
(25, 'Wash World Horsens Vejlevej', 'Vejlevej 102, 8700 Horsens', 55.833085, 9.804744),
(26, 'Wash World Højbjerg Bjødstrupvej', 'Bjødstrupvej 20E, 8270 Højbjerg', 56.107525, 10.166967),
(27, 'Wash World Ikast Europavej', 'Europavej 3, 7430 Ikast', 56.123699, 9.175422),
(28, 'Wash World Ishøj Vejleåvej', 'Vejleåvej 19, 2635 Ishøj', 55.623385, 12.321167),
(29, 'Wash World Kalundborg Holbækvej', 'Holbækvej 74, 4400 Kalundborg', 55.678767, 11.135830),
(30, 'Wash World Kolding Vejlevej 132', 'Vejlevej 132, 6000 Kolding', 55.504039, 9.458227),
(31, 'Wash World Kolding Vejlevej 251', 'Vejlevej 251, 6000 Kolding', 55.513664, 9.454697),
(32, 'Wash World Køge Københavnsvej', 'Københavnsvej 86, 4600 Køge', 55.471805, 12.181953),
(33, 'Wash World Lystrup Lægårdsvej', 'Lægårdsvej 4, 8520 Lystrup', 56.225669, 10.238525),
(34, 'Wash World Middelfart Skovsvinget', 'Skovsvinget 27c, 5500 Middelfart', 55.512013, 9.766181),
(35, 'Wash World Nakskov Løjtoftevej', 'Løjtoftevej 6, 4900 Nakskov ', 54.832475, 11.149662),
(36, 'Wash World Nyborg Storebæltsvej', 'Storebæltsvej 7F, 5800 Nyborg', 55.308498, 10.809624),
(37, 'Wash World Nykøbing Falster Guldborgsundcentret', 'Guldborgsundcentret 32, 4800 Nykøbing Falster', 54.758801, 11.851437),
(38, 'Wash World Næstved Erantisvej', 'Erantisvej 52, 4700 Næstved', 55.239173, 11.777977),
(39, 'Wash World Næstved Gl. Holstedvej', 'Gammel Holstedvej 1, 4700 Næstved', 55.249681, 11.782031),
(40, 'Wash World Nørresundby Loftbrovej', 'Loftbrovej 2, 9400 Nørresundby', 57.089142, 9.969241),
(41, 'Wash World Odense Nyborgvej', 'Nyborgvej 343, 5220 Odense', 55.391530, 10.435819),
(42, 'Wash World Odense SØ Ørbækvej', 'Ørbækvej 99, 5220 Odense SØ', 55.379874, 10.433066),
(43, 'Wash World Odense V Bystævnevej', 'Bystævnevej 5, 5200 Odense', 55.395026, 10.346525),
(44, 'Wash World Randers Messingvej', 'Messingvej 10, 8940 Randers', 56.430362, 10.053815),
(45, 'Wash World Randers Udbyhøjvej', 'Udbyhøjvej 7, 8930 Randers', 56.466047, 10.054250),
(46, 'Wash World Ribe Trojels Knæ', 'Trojels Knæ 6, 6760 Ribe', 55.351485, 8.780311),
(47, 'Wash World Ringsted Frejasvej', 'Frejasvej 43, 4100 Ringsted', 55.430669, 11.801419),
(48, 'Wash World Ringsted Nørregade', 'Nørregade 70, 4100 Ringsted', 55.451392, 11.790082),
(49, 'Wash World Risskov Ravnsøvej', 'Ravnsøvej 48B, 8240 Risskov', 56.202062, 10.244490),
(50, 'Wash World Roskilde Byleddet', 'Byleddet 2, 4000 Roskilde', 55.643709, 12.109114),
(51, 'Wash World Roskilde Ringstedvej', 'Ringstedvej 73, 4000 Roskilde', 55.628427, 12.066559),
(52, 'Wash World Silkeborg Nordre Ringvej', 'Nordre Ringvej 90, 8600 Silkeborg', 56.181413, 9.536954),
(53, 'Wash World Skive Øster Fælled vej', 'Øster Fælled vej 4, 7800 Skive', 56.561567, 9.039567),
(54, 'Wash World Slagelse Idagårdsvej', 'Idagårdsvej 2, 4200 Slagelse', 55.391735, 11.353002),
(55, 'Wash World Slagelse Smedegade', 'Smedegade 77, 4200 Slagelse', 55.407685, 11.367846),
(56, 'Wash World Sorø Apotekervej', 'Apotekervej 14, 4180 Sorø', 55.445137, 11.563255),
(57, 'Wash World Struer Bredgade', 'Bredgade 58, 7600 Struer ', 56.480435, 8.585535),
(58, 'Wash World Svendborg Nyborgvej', 'Nyborgvej 4, 5700 Svendborg', 55.062893, 10.618592),
(59, 'Wash World Svendborg Odensevej', 'Odensevej 94, 5700 Svendborg', 55.072950, 10.582398),
(60, 'Wash World Søborg Dynamovej', 'Dynamovej 4, 2860 Søborg', 55.733731, 12.459961),
(61, 'Wash World Sønderborg Centerpassagen', 'Centerpassagen 4, 6400 Sønderborg', 54.919430, 9.808034),
(62, 'Wash World Taastrup Roskildevej', 'Roskildevej 376, 2630 Taastrup', 55.658037, 12.294712),
(63, 'Wash World Thisted Østerbakken', 'Østerbakken 111, 7700 Thisted', 56.968852, 8.735134),
(64, 'Wash World Tilst Blomstervej', 'Blomstervej 2T, 8381 Tilst', 56.181787, 10.125000),
(65, 'Wash World Tønder Centerbuen', 'Centerbuen 5, 6270 Tønder', 54.951505, 8.887800),
(66, 'Wash World Vejle Soldalen', 'Soldalen 4, 7100 Vejle', 55.681238, 9.567456),
(67, 'Wash World Vejle Solkilde Allé', 'Solkilde Alle 11, 7100 Vejle', 55.723459, 9.584778),
(68, 'Wash World Viborg Falkevej', 'Falkevej 25, 8800 Viborg', 56.444161, 9.388456),
(69, 'Wash World Viborg Vognmagervej', 'Vognmagervej 21E, 8800 Viborg', 56.469366, 9.409431),
(70, 'Wash World Viby Gunnar Clausens vej', 'Gunnar Clausens Vej 2A, 8260 Viby', 56.111373, 10.125033),
(71, 'Wash World Vordingborg Valdemarsgade', 'Valdemarsgade 57, 4760 Vordingborg', 55.010855, 11.910489);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_first_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_password_hashed` varchar(255) NOT NULL,
  `user_created_at` bigint(20) UNSIGNED NOT NULL,
  `user_updated_at` bigint(20) UNSIGNED DEFAULT NULL,
  `user_verification_key` char(32) NOT NULL,
  `user_verified_at` int(10) NOT NULL,
  `user_reset_password_key` char(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_first_name`, `user_last_name`, `user_email`, `user_password_hashed`, `user_created_at`, `user_updated_at`, `user_verification_key`, `user_verified_at`, `user_reset_password_key`) VALUES
('5d318c0ef62e4742ae373cf5269b65a9', 'bb', 'cc', 'aa@aa.com', 'scrypt:32768:8:1$pTX7wRTFjbTtZKnT$b41b9b185d6436ae78e1d5c6f5cc0918466baf27725c4bd55c79ad96b2aa3792cd84450851733d7f89c3fd5891d76f618822b33c7ce932b035a21b661dadcb3b', 1779799388, 1779799388, 'f3b67fb5cfa54b5d83280b6fbd520ea0', 0, '433502d966a84403a10fc817f61a7cfed14ce9c0ad914001a08dafb236d35ff1'),
('de2faaff78fb46f2b7fdb4f316b59e1f', 'aa', 'bb', 'albertlund121@gmail.com', 'scrypt:32768:8:1$VcuoQzlIYvEId9w4$bcfd4f406350ccdf0b4c4e01bf1e179771b0c1bcce8d2c09e27f2d2f98f2ecc37a103941297abef2939687cccdcf867e60a717c3a75d661d5bfee67e8c41e99f', 1779797946, 1779797946, 'bc495d3e7cba4683aefa5237b65a3a3f', 0, '3354100939914ae68bdec80deb42901f911f38a8bca94f4fb856e774ab8ab228');

-- --------------------------------------------------------

--
-- Table structure for table `user_memberships`
--

CREATE TABLE `user_memberships` (
  `user_membership_pk` char(32) NOT NULL,
  `user_id` char(32) NOT NULL,
  `membership_id` int(11) NOT NULL,
  `start_date` bigint(20) UNSIGNED NOT NULL,
  `end_date` bigint(20) UNSIGNED DEFAULT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `washes`
--

CREATE TABLE `washes` (
  `wash_pk` char(32) NOT NULL,
  `car_id` char(32) NOT NULL,
  `membership_id` int(11) NOT NULL,
  `station_id` int(11) NOT NULL,
  `created_at` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`car_pk`),
  ADD KEY `fk_cars_user` (`user_id`);

--
-- Indexes for table `memberships`
--
ALTER TABLE `memberships`
  ADD PRIMARY KEY (`membership_pk`);

--
-- Indexes for table `stations`
--
ALTER TABLE `stations`
  ADD PRIMARY KEY (`station_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- Indexes for table `user_memberships`
--
ALTER TABLE `user_memberships`
  ADD PRIMARY KEY (`user_membership_pk`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `membership_id` (`membership_id`);

--
-- Indexes for table `washes`
--
ALTER TABLE `washes`
  ADD PRIMARY KEY (`wash_pk`),
  ADD KEY `car_id` (`car_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cars`
--
ALTER TABLE `cars`
  ADD CONSTRAINT `fk_cars_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_memberships`
--
ALTER TABLE `user_memberships`
  ADD CONSTRAINT `user_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_memberships_ibfk_2` FOREIGN KEY (`membership_id`) REFERENCES `memberships` (`membership_pk`) ON DELETE CASCADE;

--
-- Constraints for table `washes`
--
ALTER TABLE `washes`
  ADD CONSTRAINT `washes_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_pk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
