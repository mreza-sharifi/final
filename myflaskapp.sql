-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: myflaskapp
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.18.04.1-log

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
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `body` text,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `subject` int(11) DEFAULT NULL,
  `image_url` char(255) DEFAULT NULL,
  `summery` text,
  PRIMARY KEY (`id`),
  KEY `subject` (`subject`),
  CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`subject`) REFERENCES `subjects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (41,'newwwwwwwwwwwww','qqqq','<p>mmmmmmmmmmmmmmmmmmmmmmmmmmm</p>\r\n','2018-08-29 09:08:57',15,'Screenshot from 2018-06-19 05-00-51.png','<p>nnnnnnnnnnnnnnnnnnn</p>\r\n'),(42,'rfsnjmfyjkfxgjn','qqqq','<p>fyxjfhvgnjvhnj</p>\r\n','2018-08-29 09:11:46',15,'Screenshot from 2018-06-15 01-26-11.png','<p>jtydiktuyolfyuihlofvcjyuh</p>\r\n');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`mohammad`@`localhost`*/ /*!50003 TRIGGER verifyExists_article BEFORE INSERT ON articles
FOR EACH ROW 
BEGIN
IF EXISTS
(
SELECT * FROM articles  WHERE title = NEW.title
)
THEN
CALL `Insert not allowed`;
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `bits`
--

DROP TABLE IF EXISTS `bits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bits` (
  `val` enum('T','F') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bits`
--

LOCK TABLES `bits` WRITE;
/*!40000 ALTER TABLE `bits` DISABLE KEYS */;
/*!40000 ALTER TABLE `bits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `writer_id` int(11) DEFAULT NULL,
  `body` text,
  `post_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `writer_id` (`writer_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `articles` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`writer_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level`
--

DROP TABLE IF EXISTS `level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` char(25) DEFAULT NULL,
  `writing` int(11) DEFAULT NULL,
  `user_handle` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level`
--

LOCK TABLES `level` WRITE;
/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (1,'admin',1,1),(2,'writer',1,0),(3,'only_view',0,0);
/*!40000 ALTER TABLE `level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (15,'mobile','qqqq','2018-08-28 23:11:24'),(16,'laptop','qqqq','2018-08-28 23:11:34'),(17,'TV','qqqq','2018-08-28 23:11:42'),(18,'Speaker','qqqq','2018-08-28 23:11:53'),(19,'Learning','qqqq','2018-08-29 08:53:53');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`mohammad`@`localhost`*/ /*!50003 TRIGGER verifyExists_subject BEFORE INSERT ON subjects
FOR EACH ROW 
BEGIN
IF EXISTS
(
SELECT * FROM subjects  WHERE title = NEW.title
)
THEN
CALL `Insert not allowed`;
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `level_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `level_id` (`level_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`level_id`) REFERENCES `level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'fgnfn','fnfn@fgnh.com','mmmm','$5$rounds=80000$AbxQOWn.Br/VC7d3$qGLL.lNhI9SXmqlsbDxb0xMfjSNfVGevcwIZDhfxv8B','2018-07-20 09:53:13',NULL),(3,'admin','mr.sharifi1375@gmail.com','admin','$5$rounds=80000$1pOf.k03YIxgeBra$0JWPR7uUMICBTJANJB9RqvMo8QLSJqcCLDz0tBJlzV9','2018-08-02 16:02:14',1),(4,'dgfngfdn','fgnfgn','aaaa','$5$rounds=80000$JXXuSBd/XXo8.yyL$bfo.l2seQqu6j0xyBPr12Q2tgxNLb8mzocaG5pQwzM4','2018-08-03 09:56:45',2),(5,'njslkfdv','skljbvklj@gmail','mm','$5$rounds=80000$hPbRUiqQPk2CT4uU$0ai9qlFBRWjkCHB3Yu1en9xnnNRNtRK95XVsR2fLjBD','2018-08-17 12:16:42',1),(6,'admin','kkerjg@g.cm','admin','$5$rounds=80000$GA8CLfTGlHCCqOBc$fxkdDk3GNukoxRkF3i/B8b/FK7SKDv6L.7NaduZ/i3B','2018-08-20 06:46:45',1),(7,'adminn','sgsg@gmai.com','adminn','$5$rounds=80000$tPKLpR72TKFyMHWV$01gNcjt5zKlxvK8VRsWW.ysAkQbJfwkhqj0E/CJvbH.','2018-08-20 06:47:57',1),(8,'fxdbfhchb','dzfhdfghgfdchnb','xcfghnjgcjhngcvhnj','$5$rounds=80000$LuWrD.xHLf6O8AUC$7Gb4gJ2MiZNAXyhtXaV329fG.9pWSSFcKwHHnB8OQnB','2018-08-20 14:51:57',1),(9,'fhgfdcxhb','dhnfgdh','qqqq','$5$rounds=80000$NL.cbvdNGfttszId$WuwIZ.LfKgD3Do3N/WiNiaeQse3SXKuhJAeSff2plI3','2018-08-28 20:56:12',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-29 15:03:11
