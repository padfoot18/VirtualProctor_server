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
-- Table structure for table `broadcast_msg`
--

DROP TABLE IF EXISTS `broadcast_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broadcast_msg` (
  `from_id` varchar(15) DEFAULT NULL,
  `group_id` varchar(25) DEFAULT NULL,
  `msg_body` varchar(20000) DEFAULT NULL,
  `msg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `fk_user` (`from_id`),
  KEY `fk_group` (`group_id`),
  CONSTRAINT `fk_group` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`from_id`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `broadcast_msg`
--

LOCK TABLES `broadcast_msg` WRITE;
/*!40000 ALTER TABLE `broadcast_msg` DISABLE KEYS */;
/*!40000 ALTER TABLE `broadcast_msg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chats` (
  `from_user` varchar(15) DEFAULT NULL,
  `to_user` varchar(15) DEFAULT NULL,
  `msg_body` varchar(20000) DEFAULT NULL,
  `msg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `fk_from` (`from_user`),
  KEY `fk_to` (`to_user`),
  CONSTRAINT `fk_from` FOREIGN KEY (`from_user`) REFERENCES `users` (`username`),
  CONSTRAINT `fk_to` FOREIGN KEY (`to_user`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES ('1611034','1611037','hello','2019-03-30 12:28:42'),('1611034','1611032','hiii','2019-03-30 12:33:40'),('1611037','1611034','Hello. How are you doing?','2019-03-30 13:26:07'),('1611034','1611037','I am fine','2019-03-30 13:26:39'),('1611037','1611034','hey','2019-03-30 14:31:26'),('1611034','1611037','yo','2019-03-30 14:32:33');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `event` VALUES ('Abhiyantriki','event','Abhiyantriki is the Technical Fest of our college and will be held for 3 days from 5th April 2019'),('Symphony','event','Symphony is the cultural fest of our college and will be held at 19th of April'),('Prakalpa','event','Prakalpa is State Level Project Competetion on 12th May'),('MLearn','workshop','MLearn is a workshop conducted by Prof. Murtaza Patrawala for Sem 5 Students'),('CyberStud','workshop','CyberStud is a workshop for sem 4 students for Cyber Security conducted by Prof.Manish Potey on 7th April');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fees`
--

DROP TABLE IF EXISTS `fees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fees` (
  `year` int(11) DEFAULT NULL,
  `due_date` varchar(20) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fees`
--

LOCK TABLES `fees` WRITE;
/*!40000 ALTER TABLE `fees` DISABLE KEYS */;
INSERT INTO `fees` VALUES (1,'03-August-2016',150000),(2,'23-July-2017',170000),(3,'15-July-2018',180000),(4,'18-July-2019',160000);
/*!40000 ALTER TABLE `fees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `group_id` varchar(25) NOT NULL,
  `group_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES ('ty_comps_A','Ty Btech Computer, Division A'),('ty_comp_B','Ty Btech Computer, Division B');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `placement`
--

DROP TABLE IF EXISTS `placement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `placement` (
  `company_name` varchar(20) DEFAULT NULL,
  `no_student_placed` int(11) DEFAULT NULL,
  `package_offered` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placement`
--

LOCK TABLES `placement` WRITE;
/*!40000 ALTER TABLE `placement` DISABLE KEYS */;
INSERT INTO `placement` VALUES ('Morgan Stanley',10,1500000),('Accenture',100,350000),('Barclays',50,600000);
/*!40000 ALTER TABLE `placement` ENABLE KEYS */;
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
  `marks` int(11) DEFAULT NULL,
  `teacher_id` varchar(15) DEFAULT NULL,
  `attendence` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_academic_info`
--

LOCK TABLES `student_academic_info` WRITE;
/*!40000 ALTER TABLE `student_academic_info` DISABLE KEYS */;
INSERT INTO `student_academic_info` VALUES ('1611032',5,'Operating-Systems','murtaza patrawala',87,'101','50'),('1611032',5,'SPCC','suchita patil',78,'102','67'),('1611032',5,'MCAN','prasanna shete',55,'103','34'),('1611032',5,'Web-Development','swapnil patil',65,'104','84'),('1611032',5,'Data-Structure','manish potey',97,'105','65'),('1611037',4,'Cloud-Computing','manish potey',84,'109','45'),('1611037',4,'Cyber-Security','prasadini padwal',74,'106','59'),('1611037',4,'OOPM','vaibhav vasani',74,'108','83'),('1611037',4,'Data-Networks','murtaza patrawala',72,'101','63'),('1611037',4,'Machine-Learning','nirmal shinde',42,'107','75'),('1611032',4,'Cloud-Computing','manish potey',74,'109','56'),('1611032',4,'Cyber-Security','prasadini padwal',45,'106','86'),('1611032',4,'OOPM','vaibhav vasani',94,'108','76'),('1611032',4,'Data-Networks','murtaza patrawala',69,'101','65'),('1611032',4,'Machine-Learning','nirmal shinde',75,'107','45');
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
-- Table structure for table `user_to_group`
--

DROP TABLE IF EXISTS `user_to_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_to_group` (
  `username` varchar(15) DEFAULT NULL,
  `group_id` varchar(25) DEFAULT NULL,
  KEY `fk_user_to_group_1_idx` (`group_id`),
  KEY `fk_user_to_group_2_idx` (`username`),
  CONSTRAINT `fk_grp_id` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_username` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_to_group`
--

LOCK TABLES `user_to_group` WRITE;
/*!40000 ALTER TABLE `user_to_group` DISABLE KEYS */;
INSERT INTO `user_to_group` VALUES ('1611037','ty_comps_A'),('1611032','ty_comps_A');
/*!40000 ALTER TABLE `user_to_group` ENABLE KEYS */;
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
INSERT INTO `username_to_fcmId` VALUES ('1611032','e_vAClmBRBE:APA91bGdwgci5kPE9qwi_zn2CwA9yM_BNHdYZuE7hpr3VUdj8omuZfL9PSD7WgZbl7wdAdcnUyJPXK7jQWDVTsEeHeUjMNq3s1Q-_qNVlBCMW4nYGTRVGxvaH4mKNomENZK4Sm5shzpp'),('1611034','e_vAClmBRBE:APA91bGdwgci5kPE9qwi_zn2CwA9yM_BNHdYZuE7hpr3VUdj8omuZfL9PSD7WgZbl7wdAdcnUyJPXK7jQWDVTsEeHeUjMNq3s1Q-_qNVlBCMW4nYGTRVGxvaH4mKNomENZK4Sm5shzpp'),('1611037','e_vAClmBRBE:APA91bGdwgci5kPE9qwi_zn2CwA9yM_BNHdYZuE7hpr3VUdj8omuZfL9PSD7WgZbl7wdAdcnUyJPXK7jQWDVTsEeHeUjMNq3s1Q-_qNVlBCMW4nYGTRVGxvaH4mKNomENZK4Sm5shzpp');
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
  `role` varchar(15) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1611022','1234','admin','Admin'),('1611032','1234','parent','Jitendra Patel'),('1611034','1234','teacher','Murtaza Patrawala'),('1611037','1234','parent','Hemant Raul');
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

-- Dump completed on 2019-03-31  3:57:34
