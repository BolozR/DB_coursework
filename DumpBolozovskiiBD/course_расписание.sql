-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: course
-- ------------------------------------------------------
-- Server version	5.5.62

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `расписание`
--

DROP TABLE IF EXISTS `расписание`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `расписание` (
  `idПредмета` tinyint(1) unsigned NOT NULL,
  `idУчителя` tinyint(1) unsigned NOT NULL,
  `ДеньНедели` char(2) NOT NULL,
  `Время` time NOT NULL,
  `№класса` varchar(3) NOT NULL,
  `№урока` tinyint(1) NOT NULL,
  `№кабинета` tinyint(1) unsigned DEFAULT NULL,
  PRIMARY KEY (`idПредмета`,`idУчителя`,`ДеньНедели`,`№урока`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `расписание`
--

LOCK TABLES `расписание` WRITE;
/*!40000 ALTER TABLE `расписание` DISABLE KEYS */;
INSERT INTO `расписание` VALUES (1,1,'ПН','11:00:00','5А',4,1),(1,1,'ПТ','12:00:00','6А',5,255),(1,12,'ЧТ','09:00:00','8А',2,255),(2,1,'ПТ','08:00:00','7Б',1,255),(2,2,'ПТ','08:00:00','6А',1,12),(2,12,'ПН','10:00:00','5Б',3,255);
/*!40000 ALTER TABLE `расписание` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-09 19:02:41
