-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: ihome_python_04
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('2fe0bae838f3');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_area_info`
--

DROP TABLE IF EXISTS `ih_area_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_area_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_area_info`
--

LOCK TABLES `ih_area_info` WRITE;
/*!40000 ALTER TABLE `ih_area_info` DISABLE KEYS */;
INSERT INTO `ih_area_info` VALUES (NULL,NULL,1,'东城区'),(NULL,NULL,2,'西城区'),(NULL,NULL,3,'朝阳区'),(NULL,NULL,4,'海淀区'),(NULL,NULL,5,'昌平区'),(NULL,NULL,6,'丰台区'),(NULL,NULL,7,'房山区'),(NULL,NULL,8,'通州区'),(NULL,NULL,9,'顺义区'),(NULL,NULL,10,'大兴区'),(NULL,NULL,11,'怀柔区'),(NULL,NULL,12,'平谷区'),(NULL,NULL,13,'密云区'),(NULL,NULL,14,'延庆区'),(NULL,NULL,15,'石景山区');
/*!40000 ALTER TABLE `ih_area_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_facility_info`
--

DROP TABLE IF EXISTS `ih_facility_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_facility_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_facility_info`
--

LOCK TABLES `ih_facility_info` WRITE;
/*!40000 ALTER TABLE `ih_facility_info` DISABLE KEYS */;
INSERT INTO `ih_facility_info` VALUES (NULL,NULL,1,'无线网络'),(NULL,NULL,2,'热水淋浴'),(NULL,NULL,3,'空调'),(NULL,NULL,4,'暖气'),(NULL,NULL,5,'允许吸烟'),(NULL,NULL,6,'饮水设备'),(NULL,NULL,7,'牙具'),(NULL,NULL,8,'香皂'),(NULL,NULL,9,'拖鞋'),(NULL,NULL,10,'手纸'),(NULL,NULL,11,'毛巾'),(NULL,NULL,12,'沐浴露、洗发露'),(NULL,NULL,13,'冰箱'),(NULL,NULL,14,'洗衣机'),(NULL,NULL,15,'电梯'),(NULL,NULL,16,'允许做饭'),(NULL,NULL,17,'允许带宠物'),(NULL,NULL,18,'允许聚会'),(NULL,NULL,19,'门禁系统'),(NULL,NULL,20,'停车位'),(NULL,NULL,21,'有线网络'),(NULL,NULL,22,'电视'),(NULL,NULL,23,'浴缸');
/*!40000 ALTER TABLE `ih_facility_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_facility`
--

DROP TABLE IF EXISTS `ih_house_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `ih_house_facility_ibfk_1` FOREIGN KEY (`facility_id`) REFERENCES `ih_facility_info` (`id`),
  CONSTRAINT `ih_house_facility_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_facility`
--

LOCK TABLES `ih_house_facility` WRITE;
/*!40000 ALTER TABLE `ih_house_facility` DISABLE KEYS */;
INSERT INTO `ih_house_facility` VALUES (2,1),(3,1),(4,1),(5,1),(2,2),(3,2),(2,3),(3,3),(4,3),(5,3),(2,4),(3,4),(5,4),(2,5),(3,5),(4,5),(5,5),(2,6),(3,6),(6,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(2,8),(3,8),(7,8),(2,9),(3,9),(5,9),(2,10),(3,10),(5,10),(2,11),(3,11),(5,11),(7,11),(2,12),(3,12),(7,12),(2,13),(3,13),(5,13),(6,13),(7,13),(2,14),(3,14),(4,14),(5,14),(6,14),(2,15),(3,15),(5,15),(7,15),(2,16),(3,16),(2,17),(3,17),(5,17),(2,18),(3,18),(4,18),(6,18),(2,19),(3,19),(5,19),(6,19),(2,20),(3,20),(5,20),(7,20),(2,21),(3,21),(5,21),(7,21),(2,22),(3,22),(5,22),(2,23),(3,23),(5,23),(6,23);
/*!40000 ALTER TABLE `ih_house_facility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_image`
--

DROP TABLE IF EXISTS `ih_house_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_image` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `ih_house_image_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_image`
--

LOCK TABLES `ih_house_image` WRITE;
/*!40000 ALTER TABLE `ih_house_image` DISABLE KEYS */;
INSERT INTO `ih_house_image` VALUES ('2019-07-21 08:35:12','2019-07-21 08:35:12',1,2,'Fi556M07BT0kVdYEaqCIvkm2Hrw-'),('2019-07-21 08:35:22','2019-07-21 08:35:22',2,2,'FmnBWqwBt9K1L2w0N6a7m-b0VIaw'),('2019-07-21 08:35:32','2019-07-21 08:35:32',3,2,'Fv-DlZJXfWUpl6-Ag3jPolKGIllC'),('2019-07-21 08:35:40','2019-07-21 08:35:40',4,2,'FliA7MTXEwE0hlIMTefsRrTqpYGv'),('2019-07-21 08:35:49','2019-07-21 08:35:49',5,2,'FlAuGs37r0TJD86JNqv9jSp6W5Fy'),('2019-07-21 08:35:55','2019-07-21 08:35:55',6,2,'FlAuGs37r0TJD86JNqv9jSp6W5Fy'),('2019-07-21 10:10:45','2019-07-21 10:10:45',7,3,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn'),('2019-07-21 10:13:39','2019-07-21 10:13:39',8,4,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2019-07-21 15:19:29','2019-07-21 15:19:29',9,5,'Fv6yrltTqc-j3fioxvOo5tQRHqN1'),('2019-07-21 15:20:48','2019-07-21 15:20:48',10,6,'FgD4hkeySPVea6Kbjl-KX7Uvi2AG'),('2019-07-21 15:22:03','2019-07-21 15:22:03',11,7,'FjlaS4rvABoczc6QvoxEY53LQyt1');
/*!40000 ALTER TABLE `ih_house_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_info`
--

DROP TABLE IF EXISTS `ih_house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `title` varchar(64) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `acreage` int(11) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `beds` varchar(64) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `min_days` int(11) DEFAULT NULL,
  `max_days` int(11) DEFAULT NULL,
  `order_count` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ih_house_info_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `ih_area_info` (`id`),
  CONSTRAINT `ih_house_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_info`
--

LOCK TABLES `ih_house_info` WRITE;
/*!40000 ALTER TABLE `ih_house_info` DISABLE KEYS */;
INSERT INTO `ih_house_info` VALUES ('2019-07-21 08:34:56','2019-07-22 09:57:39',2,2,17,'房租月付 朝阳门 东八宝胡同小区 品质小区 双周保洁 宜家风',30000,'朝阳门 东八宝胡同小区\r\n没有费，直租房 特价\r\n\r\n装修：工业风格精装修，温馨舒适，精装大主卧，南向采光\r\n家配套：配备品牌家具家电、配套床垫、抱枕、台灯、壁灯、减轻疲劳桌椅、衣柜、空调、洗衣机、冰箱和厨房，高速宽带。\r\n环境：小区安静舒适，适合居家\r\n该房源，可月付',3,27,'直租房 特价',3,'精装大主卧',300000,2,7,1,'Fi556M07BT0kVdYEaqCIvkm2Hrw-'),('2019-07-21 10:10:25','2019-07-21 10:10:45',3,2,18,'west',20000,'west-city',3,50,'complexe-simple',3,'double-bed',300000,1,0,0,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn'),('2019-07-21 10:13:31','2019-07-21 10:13:39',4,2,19,'chaoyang',27000,'chaoyang-city',2,15,'simple',1,'simple-bed',50000,1,0,0,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2019-07-21 15:19:07','2019-07-21 15:19:29',5,2,17,'haidian',40000,'haidian-test',6,200,'simple',8,'double-bed',50000,1,0,0,'Fv6yrltTqc-j3fioxvOo5tQRHqN1'),('2019-07-21 15:20:35','2019-07-21 15:20:48',6,2,21,'changping',28000,'changping-test',4,100,'simple',5,'double-bed',80000,1,0,0,'FgD4hkeySPVea6Kbjl-KX7Uvi2AG'),('2019-07-21 15:21:55','2019-07-21 15:22:03',7,2,22,'fengtai',18000,'fengtai-test',3,120,'simple',3,'double-bed',40000,1,0,0,'FjlaS4rvABoczc6QvoxEY53LQyt1');
/*!40000 ALTER TABLE `ih_house_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_order_info`
--

DROP TABLE IF EXISTS `ih_order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_order_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT NULL,
  `comment` text,
  `trade_no` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_ih_order_info_status` (`status`),
  CONSTRAINT `ih_order_info_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`),
  CONSTRAINT `ih_order_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_order_info`
--

LOCK TABLES `ih_order_info` WRITE;
/*!40000 ALTER TABLE `ih_order_info` DISABLE KEYS */;
INSERT INTO `ih_order_info` VALUES ('2019-07-21 18:55:52','2019-07-21 18:57:29',1,1,7,'2019-07-21 00:00:00','2019-07-22 00:00:00',2,18000,36000,'REJECTED',NULL,NULL),('2019-07-21 18:56:29','2019-07-21 18:57:14',2,1,6,'2019-07-24 00:00:00','2019-07-25 00:00:00',2,28000,56000,'WAIT_PAYMENT',NULL,NULL),('2019-07-22 09:06:23','2019-07-22 09:09:24',3,1,5,'2019-07-22 00:00:00','2019-07-30 00:00:00',9,40000,360000,'WAIT_PAYMENT',NULL,NULL),('2019-07-22 09:12:31','2019-07-22 09:14:12',4,1,4,'2019-07-22 00:00:00','2019-07-30 00:00:00',9,27000,243000,'WAIT_PAYMENT',NULL,NULL),('2019-07-22 09:47:31','2019-07-22 09:57:39',5,1,2,'2019-07-22 00:00:00','2019-07-30 00:00:00',9,30000,270000,'COMPLETE','not bad','2019072222001411901000022577');
/*!40000 ALTER TABLE `ih_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_user_profile`
--

DROP TABLE IF EXISTS `ih_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_user_profile` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `real_name` varchar(32) DEFAULT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_user_profile`
--

LOCK TABLES `ih_user_profile` WRITE;
/*!40000 ALTER TABLE `ih_user_profile` DISABLE KEYS */;
INSERT INTO `ih_user_profile` VALUES ('2019-07-19 11:27:04','2019-07-21 16:43:42',1,'kk','pbkdf2:sha256:50000$yb0HSUOo$e479c50a4a56575343c8ac8cf65ef6946c71c56917b54c2c2baa4e990af0857f','18611111111',NULL,NULL,'FmT-Qpi7yYr_2GHYOnS6n4r5h8jY'),('2019-07-19 11:57:52','2019-07-21 08:43:12',2,'kk.zhang','pbkdf2:sha256:50000$RSlds1Q3$a0b93c053af64899f6a8d538833963121dbf37e28137516e85ae485b096fe0b1','18611111112','jams','130111111111111111','FituDChCYaxXQtc8WjuHZNcQP7d-'),('2019-07-19 13:21:31','2019-07-19 13:21:31',3,'18611111113','pbkdf2:sha256:50000$21UDrhzc$792b0f35bc63f971486f8c742fbf26c3f593a47875eedfed68075ab2d28ab12d','18611111113',NULL,NULL,NULL),('2019-07-22 16:40:54','2019-07-22 16:40:54',4,'18611111114','pbkdf2:sha256:50000$OkdaMRME$dd12659ab3c9c20a293613f6ca961b8ececd288b3a617b369e1b2cdf8180b3c8','18611111114',NULL,NULL,NULL);
/*!40000 ALTER TABLE `ih_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-22 16:54:52
