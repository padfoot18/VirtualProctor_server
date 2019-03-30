-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: VirtualProctor
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

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
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `name` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_academic_info`
--

DROP TABLE IF EXISTS `student_academic_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_academic_info` (
  `username` varchar(20) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `subject` varchar(20) DEFAULT NULL,
  `teacher` varchar(20) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_academic_info`
--

LOCK TABLES `student_academic_info` WRITE;
/*!40000 ALTER TABLE `student_academic_info` DISABLE KEYS */;
INSERT INTO `student_academic_info` VALUES ('1611032',5,'Operating Systems','Murtaza Patrawala',87),('1611032',5,'SPCC','Suchita Patil',78),('1611032',5,'MCAN','Prasanna Shete',55),('1611032',5,'Web Development','Swapnil Patil',65),('1611032',5,'Data Structure','Manish Potey',97),('1611037',4,'Cloud Computing','Manish Potey',84),('1611037',4,'Cyber Security','Prasidini Padwal',74),('1611037',4,'OOPM','Vaibhav Vasani',74),('1611037',4,'Data Networks','Murtaza Patrawala',72),('1611037',4,'Machine Learning','Nirmal Shinde',42),('1611032',4,'Cloud Computing','Manish Potey',74),('1611032',4,'Cyber Security','Prasidini Padwal',45),('1611032',4,'OOPM','Vaibhav Vasani',94),('1611032',4,'Data Networks','Murtaza Patrawala',69),('1611032',4,'Machine Learning','Nirmal Shinde',75);
/*!40000 ALTER TABLE `student_academic_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_personal_info`
--

DROP TABLE IF EXISTS `student_personal_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_personal_info` (
  `username` varchar(20) DEFAULT NULL,
  `student_name` varchar(20) DEFAULT NULL,
  `parent_name` varchar(20) DEFAULT NULL,
  `current_sem` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_personal_info`
--

LOCK TABLES `student_personal_info` WRITE;
/*!40000 ALTER TABLE `student_personal_info` DISABLE KEYS */;
INSERT INTO `student_personal_info` VALUES ('1611032','Harsh','Jitendra','5'),('1611037','Tanay','Hemant','4');
/*!40000 ALTER TABLE `student_personal_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `username_to_fcmId`
--

DROP TABLE IF EXISTS `username_to_fcmId`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `username_to_fcmId` (
  `username` varchar(15) NOT NULL,
  `fcm_id` varchar(1024) NOT NULL,
  PRIMARY KEY (`username`,`fcm_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `username_to_fcmId`
--

LOCK TABLES `username_to_fcmId` WRITE;
/*!40000 ALTER TABLE `username_to_fcmId` DISABLE KEYS */;
/*!40000 ALTER TABLE `username_to_fcmId` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `role` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1611022','1234','admin'),('1611037','1234','parent'),('1611034','1234','teacher'),('1611032','1234','parent');
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

-- Dump completed on 2019-03-30 16:20:39
