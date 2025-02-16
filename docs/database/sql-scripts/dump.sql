-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: occitanie_yield_db
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `communes_data`
--

DROP TABLE IF EXISTS `communes_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `communes_data` (
  `INSEE_COM` char(5) NOT NULL,
  `INSEE_DEP` char(2) NOT NULL,
  `NOM_COM_M` varchar(100) NOT NULL,
  `POPULATION` int NOT NULL,
  `PrixMoyen_M2_2223` decimal(10,2) NOT NULL,
  `Prixm2Moyen_2022` decimal(10,2) NOT NULL,
  `Prixm2Moyen_2023` decimal(10,2) NOT NULL,
  `loyer_apparts` decimal(10,2) NOT NULL,
  `loyer_maisons` decimal(10,2) NOT NULL,
  `Rendement_locatif_apparts` decimal(10,2) NOT NULL,
  `Rendement_locatif_maisons` decimal(10,2) NOT NULL,
  PRIMARY KEY (`INSEE_COM`),
  KEY `fk_insee_dep` (`INSEE_DEP`),
  CONSTRAINT `fk_insee_dep` FOREIGN KEY (`INSEE_DEP`) REFERENCES `departements_data` (`INSEE_DEP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communes_data`
--

LOCK TABLES `communes_data` WRITE;
/*!40000 ALTER TABLE `communes_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `communes_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departements_data`
--

DROP TABLE IF EXISTS `departements_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departements_data` (
  `INSEE_DEP` char(2) NOT NULL,
  `NOM_DEP` varchar(100) NOT NULL,
  `Taux_Chomage_2022` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`INSEE_DEP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departements_data`
--

LOCK TABLES `departements_data` WRITE;
/*!40000 ALTER TABLE `departements_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `departements_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-16 10:00:31
