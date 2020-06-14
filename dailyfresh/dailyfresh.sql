set foreign_key_checks=0;

--
-- Dumping data for table `df_goods`
--

LOCK TABLES `df_goods` WRITE;
/*!40000 ALTER TABLE `df_goods` DISABLE KEYS */;
INSERT INTO `df_goods` VALUES (1,'2017-11-15 03:03:05.257969','2017-11-15 03:03:05.258130',0,'草莓','<p><strong>很不错的草莓</strong></p>'),(2,'2017-11-15 03:05:36.964951','2017-11-15 03:05:36.965129',0,'葡萄',''),(3,'2017-11-15 03:05:52.323866','2017-11-15 03:05:52.323949',0,'柠檬',''),(4,'2017-11-15 03:06:01.267481','2017-11-15 03:06:01.267615',0,'奇异果',''),(5,'2017-11-15 03:06:30.418683','2017-11-15 03:06:30.418789',0,'大青虾',''),(6,'2017-11-15 03:06:35.994464','2017-11-15 03:06:35.994567',0,'秋刀鱼',''),(7,'2017-11-15 03:06:48.115318','2017-11-15 03:06:48.115410',0,'扇贝',''),(8,'2017-11-15 03:07:03.057514','2017-11-15 03:07:03.057601',0,'基围虾',''),(9,'2017-11-15 03:07:36.306725','2017-11-15 03:07:36.306926',0,'猪肉',''),(10,'2017-11-15 03:07:39.056064','2017-11-15 03:07:39.056145',0,'牛肉',''),(11,'2017-11-15 03:07:41.955755','2017-11-15 03:07:41.955833',0,'羊肉',''),(12,'2017-11-15 03:07:44.741474','2017-11-15 03:07:44.741574',0,'牛排',''),(13,'2017-11-15 03:07:51.748699','2017-11-15 03:07:51.748828',0,'鸡蛋',''),(14,'2017-11-15 03:07:56.413773','2017-11-15 03:07:56.413853',0,'鸡肉',''),(15,'2017-11-15 03:07:59.568405','2017-11-15 03:07:59.568554',0,'鸭蛋',''),(16,'2017-11-15 03:08:03.020608','2017-11-15 03:08:03.020764',0,'鸡腿',''),(17,'2017-11-15 03:08:10.063820','2017-11-15 03:08:10.063898',0,'白菜',''),(18,'2017-11-15 03:08:13.315906','2017-11-15 03:08:13.316025',0,'芹菜',''),(19,'2017-11-15 03:08:16.351445','2017-11-15 03:08:16.351526',0,'香菜',''),(20,'2017-11-15 03:08:24.232660','2017-11-15 03:08:24.232743',0,'冬瓜',''),(21,'2017-11-15 03:08:36.939678','2017-11-15 03:08:36.940113',0,'鱼丸',''),(22,'2017-11-15 03:08:43.194862','2017-11-15 03:08:43.194985',0,'蟹棒',''),(23,'2017-11-15 03:08:50.771785','2017-11-15 03:08:50.771931',0,'虾丸',''),(24,'2017-11-15 03:09:01.546052','2017-11-15 03:09:01.546152',0,'速冻水饺',''),(25,'2017-11-14 08:50:50.383071','2017-11-14 08:50:50.383115',0,'芒果',''),(26,'2017-11-17 07:54:26.657410','2017-11-17 07:54:26.657443',0,'鹌鹑蛋',''),(27,'2017-11-17 07:54:35.205668','2017-11-17 07:54:35.205703',0,'鹅蛋',''),(28,'2017-11-17 07:54:46.756236','2017-11-17 07:54:46.756272',0,'红辣椒','');
/*!40000 ALTER TABLE `df_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_goods_image`
--

LOCK TABLES `df_goods_image` WRITE;
/*!40000 ALTER TABLE `df_goods_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_goods_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_goods_sku`
--

LOCK TABLES `df_goods_sku` WRITE;
/*!40000 ALTER TABLE `df_goods_sku` DISABLE KEYS */;
INSERT INTO `df_goods_sku` VALUES (1,'2017-11-15 03:10:14.045538','2017-11-14 08:24:49.138489',0,'草莓 500g','草莓简介',10.00,'500g','group1/M00/00/03/wKgKs1yAibqAaLUUAAEc8FlxEvU0030490',98,0,1,1,1),(2,'2017-11-15 03:11:04.490384','2017-11-14 08:44:43.484243',0,'盒装草莓','草莓简介',20.00,'盒','group1/M00/00/03/wKgKs1yAibGAZtmaAAAljHPuXJg3059120',10,0,1,1,1),(3,'2017-11-15 03:12:32.165020','2017-11-14 08:25:22.505620',0,'葡萄','葡萄简介',20.00,'500g','group1/M00/00/03/wKgKs1yAiauADIASAAAjjiYTEkw3448740',7,0,1,2,1),(4,'2017-11-15 03:13:16.457844','2017-11-14 08:25:34.181904',0,'柠檬','简介',32.00,'500g','group1/M00/00/03/wKgKs1yAiZWARkUJAAAgnaeGwNQ8050600',12,0,1,3,1),(5,'2017-11-15 03:14:05.799352','2017-11-14 08:25:56.427676',0,'奇异果','简介',12.12,'500g','group1/M00/00/03/wKgKs1yAiY-AUYZ4AAAeuLYy0pU6642027',12,0,1,4,1),(6,'2017-11-15 03:15:09.971968','2017-11-14 08:26:09.113586',0,'大青虾','简介',34.00,'500g','group1/M00/00/03/wKgKs1yAiVKAZXBmAAAk0DN4-yE1037094',12,0,1,5,2),(7,'2017-11-15 03:15:53.812181','2017-11-14 08:26:19.094675',0,'北海道秋刀鱼','简介',50.00,'500g','group1/M00/00/03/wKgKs1yAiTKALQySAAAkaP_7_185626592',15,0,1,6,2),(8,'2017-11-15 03:16:24.763232','2017-11-14 08:26:31.121824',0,'扇贝','简介',56.60,'500g','group1/M00/00/03/wKgKs1yAiSuADpwqAAAk8WCqqmI0954846',13,0,1,7,2),(9,'2017-11-15 03:17:13.426611','2017-11-14 08:26:58.739624',0,'基围虾','简介',100.90,'500g','group1/M00/00/03/wKgKs1yAiSCAY_u1AAA5OS4Kl4c2359568',14,0,1,8,2),(10,'2017-11-15 03:17:47.656066','2017-11-14 08:29:56.158261',0,'猪肉','简介',23.99,'500g','group1/M00/00/03/wKgKs1yAiRSAdnxTAAEVpb1YHUE3108660',100,0,1,9,3),(11,'2017-11-15 03:18:15.497630','2017-11-14 08:31:27.169999',0,'牛肉','简介',34.99,'500g','group1/M00/00/03/wKgKs1yAiQSARwwpAAEExAU4yXU9738923',100,0,1,10,3),(12,'2017-11-15 03:18:44.453933','2017-11-14 08:32:22.493340',0,'羊肉','简介',56.99,'500g','group1/M00/00/03/wKgKs1yAiOeAH_HHAAB6NOQDrpk7645511',100,0,1,11,3),(13,'2017-11-15 03:19:10.209472','2017-11-14 08:33:15.061544',0,'牛排','简介',99.99,'500g','group1/M00/00/03/wKgKs1yAiJmAfUreAACwa3rCDPQ7991948',100,0,1,12,3),(14,'2017-11-15 03:19:44.020204','2017-11-14 08:34:31.275370',0,'盒装鸡蛋','简介',23.00,'500g','group1/M00/00/03/wKgKs1yAiIuAc6o_AADUKbwLSqY2461183',100,0,1,13,4),(15,'2017-11-15 03:20:20.962831','2017-11-14 08:35:21.725162',0,'鸡肉','简介',32.00,'500g','group1/M00/00/03/wKgKs1yAiPWAOcVUAADUY5hC_sI5972080',100,0,1,14,4),(16,'2017-11-15 03:20:53.724305','2017-11-14 08:37:27.336911',0,'鸭蛋','简介',45.00,'盒','group1/M00/00/03/wKgKs1yAiFSAKvl6AAFC_2tSkFo6349562',121,0,1,15,4),(17,'2017-11-15 03:21:22.965398','2017-11-14 08:38:08.440778',0,'鸡腿','简介',45.00,'500g','group1/M00/00/03/wKgKs1yAiEOAB19MAAA2_p7G96w3287129',12,0,1,16,4),(18,'2017-11-15 03:22:04.462490','2017-11-14 08:38:45.119926',0,'白菜','简介',4.50,'500g','group1/M00/00/03/wKgKs1yAiDyAd64rAADWHYeKaNI1147858',100,0,1,17,5),(19,'2017-11-15 03:22:31.745392','2017-11-14 08:39:40.030728',0,'芹菜','简介',3.50,'500g','group1/M00/00/03/wKgKs1yAiCmAX6dcAACIrzuaK641721221',12,0,1,18,5),(20,'2017-11-15 03:23:21.161526','2017-11-14 08:40:08.185684',0,'香菜','简介',7.90,'500g','group1/M00/00/03/wKgKs1yAiB-AN8oRAACNpHC0IEY3038323',100,0,1,19,5),(21,'2017-11-15 03:23:46.986158','2017-11-14 08:40:38.330247',0,'冬瓜','简介',12.99,'500g','group1/M00/00/03/wKgKs1yAh_6AI4sFAAENHrNG1-s7667015',100,0,1,20,5),(22,'2017-11-15 03:24:10.445214','2017-11-14 08:41:19.155821',0,'鱼丸','简介',66.00,'500g','group1/M00/00/03/wKgKs1yAh_GAfe69AADZQphQJ2o0104099',12,0,1,21,6),(23,'2017-11-15 03:24:37.927158','2017-11-14 08:41:59.658787',0,'蟹棒','简介',68.00,'500g','group1/M00/00/03/wKgKs1yAh-SAWX4CAABxy5vKkgY2542846',100,0,1,22,6),(24,'2017-11-15 03:25:18.235816','2017-11-14 08:42:25.868409',0,'虾丸','简介',89.99,'500g','group1/M00/00/03/wKgKs1yAh9iALACfAABICav_wjk9694582',100,0,1,23,6),(25,'2017-11-15 03:25:56.170531','2017-11-14 08:43:18.768380',0,'速冻水饺','简介',20.00,'袋','group1/M00/00/03/wKgKs1yAh8KAGENGAACMoBJXjDs3939941',100,0,1,24,6),(26,'2017-11-14 08:53:00.188619','2017-11-14 08:53:00.188652',0,'越南芒果','新鲜越南芒果',29.90,'2.5kg','group1/M00/00/03/wKgKs1yAhniAVL9CAAByzTJcTjM5349871',100,0,1,25,1),(27,'2017-11-17 07:57:00.677981','2017-11-17 07:57:00.678022',0,'鹌鹑蛋','简介',39.80,'126枚','group1/M00/00/03/wKgKs1yAhmaAJaQNAAGZ6KapWiA4760127',100,0,1,26,4),(28,'2017-11-17 07:58:18.361078','2017-11-17 07:58:18.361122',0,'鹅蛋','简介',49.90,'6枚','group1/M00/00/03/wKgKs1yAhl2ADd-bAADg_NUp5b45405323',80,0,1,27,4),(29,'2017-11-17 07:59:48.998394','2017-11-17 07:59:48.998431',0,'红辣椒','简介',11.00,'2.5kg','group1/M00/00/02/wKgKs1yAhk2AeSb2AAHXO8pdocY8245225',150,0,1,28,5);
/*!40000 ALTER TABLE `df_goods_sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_goods_type`
--

LOCK TABLES `df_goods_type` WRITE;
/*!40000 ALTER TABLE `df_goods_type` DISABLE KEYS */;
INSERT INTO `df_goods_type` VALUES (1,'2017-11-14 05:02:09.888544','2017-11-14 05:02:09.888598',0,'新鲜水果','fruit','group1/M00/00/02/wKgKs1yAhaCAEmNHAAAmv27pX4k0688785'),(2,'2017-11-14 05:04:32.069517','2017-11-14 05:04:32.069561',0,'海鲜水产','seafood','group1/M00/00/02/wKgKs1yAhdKAVRz4AABHr3RQqFs8160016'),(3,'2017-11-14 05:05:34.514415','2017-11-14 05:05:34.514449',0,'猪牛羊肉','meet','group1/M00/00/02/wKgKs1yAhd2AeH8KAAAy1Tlm9So6560898'),(4,'2017-11-14 05:05:58.366135','2017-11-14 05:05:58.366170',0,'禽类蛋品','egg','group1/M00/00/02/wKgKs1yAheaAe_XgAAAqR4DoSUg0209177'),(5,'2017-11-14 05:06:32.561861','2017-11-14 05:06:32.561895',0,'新鲜蔬菜','vegetables','group1/M00/00/02/wKgKs1yAhe-AFrHPAAA-0ZoYkpM7553665'),(6,'2017-11-14 05:06:55.562634','2017-11-14 05:06:55.562673',0,'速冻食品','ice','group1/M00/00/02/wKgKs1yAhWSAPKQ7AAA3sZPrVzQ1143283');
/*!40000 ALTER TABLE `df_goods_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_index_banner`
--

LOCK TABLES `df_index_banner` WRITE;
/*!40000 ALTER TABLE `df_index_banner` DISABLE KEYS */;
INSERT INTO `df_index_banner` VALUES (1,'2017-11-14 08:48:05.549864','2017-11-14 08:48:05.549896',0,'group1/M00/00/03/wKgKs1yAii6AHkJkAACpB-LsCdE5239004',3,5),(2,'2017-11-14 08:53:26.498965','2017-11-14 08:53:26.499001',0,'group1/M00/00/03/wKgKs1yAijiAK_ZwAAC3B-z8J2c6762774',1,26),(3,'2017-11-14 08:53:40.586457','2017-11-14 08:53:40.586490',0,'group1/M00/00/03/wKgKs1yAijyANJrYAAETwXb_pso3067006',0,13),(4,'2017-11-14 08:54:02.805958','2017-11-14 08:54:02.805992',0,'group1/M00/00/03/wKgKs1yAikKAdVO7AAD0akkXmFo9282293',2,9);
/*!40000 ALTER TABLE `df_index_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_index_promotion`
--

LOCK TABLES `df_index_promotion` WRITE;
/*!40000 ALTER TABLE `df_index_promotion` DISABLE KEYS */;
INSERT INTO `df_index_promotion` VALUES (1,'2017-11-14 08:56:21.863522','2017-11-17 08:29:08.554743',0,'吃货暑假趴','#','group1/M00/00/02/wKgKs1yAhQqAc_cLAAA2pLUeB600980962',2),(2,'2017-11-14 08:56:53.522161','2017-11-14 08:56:53.522193',0,'盛夏尝鲜季','#','group1/M00/00/02/wKgKs1yAhTCANFPTAAA98yvCs1I5518468',1);
/*!40000 ALTER TABLE `df_index_promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_index_type_goods`
--

LOCK TABLES `df_index_type_goods` WRITE;
/*!40000 ALTER TABLE `df_index_type_goods` DISABLE KEYS */;
INSERT INTO `df_index_type_goods` VALUES (1,'2017-11-14 08:57:41.509910','2017-11-14 08:57:41.509945',0,1,0,2,1),(2,'2017-11-14 08:57:50.129355','2017-11-14 08:57:50.129388',0,1,1,3,1),(3,'2017-11-14 08:58:00.896427','2017-11-14 08:58:00.896459',0,1,2,5,1),(4,'2017-11-14 08:58:20.417072','2017-11-14 08:58:20.417107',0,1,3,4,1),(5,'2017-11-14 08:58:32.934165','2017-11-14 08:58:32.934197',0,0,0,2,1),(6,'2017-11-14 08:58:53.943189','2017-11-14 08:58:53.943227',0,0,1,4,1),(7,'2017-11-14 08:59:16.396829','2017-11-14 08:59:16.396864',0,1,0,6,2),(8,'2017-11-14 08:59:25.723510','2017-11-14 08:59:25.723545',0,1,1,7,2),(9,'2017-11-14 08:59:37.353278','2017-11-14 08:59:37.353315',0,1,2,8,2),(10,'2017-11-14 08:59:48.082119','2017-11-14 09:30:28.117330',0,1,3,9,2),(11,'2017-11-14 08:59:59.725972','2017-11-14 08:59:59.726006',0,0,0,9,2),(12,'2017-11-14 09:00:11.685051','2017-11-14 09:00:11.685098',0,0,1,8,2),(13,'2017-11-14 09:00:20.409490','2017-11-14 09:00:20.409522',0,1,0,10,3),(15,'2017-11-14 09:00:41.325634','2017-11-14 09:00:41.325668',0,1,2,12,3),(16,'2017-11-14 09:00:56.193991','2017-11-14 09:00:56.194023',0,1,3,13,3),(17,'2017-11-14 09:01:09.550978','2017-11-14 09:01:09.551016',0,0,0,15,3),(18,'2017-11-14 09:01:18.798219','2017-11-14 09:01:18.798251',0,1,1,17,3),(19,'2017-11-14 09:01:29.182673','2017-11-14 09:01:29.182705',0,1,0,14,4),(20,'2017-11-14 09:01:44.702111','2017-11-14 09:01:44.702146',0,1,1,16,4),(21,'2017-11-14 09:02:01.490018','2017-11-14 09:02:01.490053',0,0,0,14,4),(22,'2017-11-14 09:02:14.000306','2017-11-14 09:02:14.000344',0,0,1,16,4),(23,'2017-11-14 09:02:29.300733','2017-11-14 09:02:29.300768',0,1,0,18,5),(24,'2017-11-14 09:02:38.655411','2017-11-14 09:02:38.655444',0,1,1,19,5),(25,'2017-11-14 09:02:48.641048','2017-11-14 09:02:48.641080',0,1,2,20,5),(26,'2017-11-14 09:03:01.896718','2017-11-14 09:03:01.896759',0,0,0,20,5),(27,'2017-11-14 09:03:14.583044','2017-11-14 09:03:14.583086',0,0,1,19,5),(28,'2017-11-14 09:03:27.597171','2017-11-14 09:03:27.597206',0,1,0,22,6),(29,'2017-11-14 09:03:37.078417','2017-11-14 09:03:37.078451',0,1,1,23,6),(30,'2017-11-14 09:03:48.459266','2017-11-14 09:03:48.459299',0,1,2,24,6),(31,'2017-11-14 09:03:58.834392','2017-11-14 09:03:58.834428',0,1,3,25,6),(32,'2017-11-14 09:04:11.118584','2017-11-14 09:04:11.118628',0,0,0,23,6),(33,'2017-11-14 09:04:21.235831','2017-11-14 09:04:21.235887',0,0,1,25,6),(34,'2017-11-17 08:00:09.522776','2017-11-17 08:00:09.522811',0,1,2,27,4),(35,'2017-11-17 08:00:19.382093','2017-11-17 08:00:19.382125',0,1,3,28,4),(36,'2017-11-17 08:00:31.352237','2017-11-17 08:00:31.352274',0,1,3,29,5);
/*!40000 ALTER TABLE `df_index_type_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_order_goods`
--

LOCK TABLES `df_order_goods` WRITE;
/*!40000 ALTER TABLE `df_order_goods` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_order_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_order_info`
--

LOCK TABLES `df_order_info` WRITE;
/*!40000 ALTER TABLE `df_order_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_user`
--

LOCK TABLES `df_user` WRITE;
/*!40000 ALTER TABLE `df_user` DISABLE KEYS */;
INSERT INTO `df_user` VALUES (1,'pbkdf2_sha256$20000$JCo477SbBoIA$hbjnCZodIdqKfsG12ZbhRF/CcRY2+HvusKwjFNMWXZ8=','2019-03-07 12:10:51.867533',1,'admin','','','a2205963007@hotmail.com',1,1,'2019-03-07 02:37:20.463739','2019-03-07 02:37:20.482823','2019-03-07 02:37:20.482872',0),(2,'pbkdf2_sha256$20000$y4aCqLVcLLAL$GxJZ4Bs8LL0SJ9xmwN0C8HI73zIxhCN1MWx+l+jkPls=',NULL,0,'lijunjie','','','a2205963007@hotmail.com',0,1,'2019-03-07 06:21:57.994069','2019-03-07 06:21:58.013943','2019-03-07 06:21:58.013968',0),(3,'pbkdf2_sha256$20000$PBKF0QEwH1sl$EBGUTFqkl33wUAm2+Rny5bnNT5PrE4nVTaT1RNGfZs0=',NULL,0,'lijunjie01','','','a2205963007@hotmail.com',0,1,'2019-03-07 06:23:54.547053','2019-03-07 06:23:54.566766','2019-03-07 06:23:54.566795',0),(4,'pbkdf2_sha256$20000$6gseqMyrRS70$LNJ4/Nv4OvLoIm8gbCyQg7KR8kbE27xMObAjK5gRHyQ=','2019-03-07 06:43:06.588150',0,'lijunjie02','','','a2205963007@hotmail.com',0,1,'2019-03-07 06:26:01.709155','2019-03-07 06:26:01.728089','2019-03-07 06:26:01.728113',0),(5,'pbkdf2_sha256$20000$Sdh02BoW5WG4$aSY90Zil79pgfbQkRHOYKYf8RKhF1r8EufhfS4tPzH0=',NULL,0,'lijunjie04','','','a2205963007@hotmail.com',0,1,'2019-03-07 11:12:24.721212','2019-03-07 11:12:24.741569','2019-03-07 11:12:24.741588',0);
/*!40000 ALTER TABLE `df_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `df_user_groups`
--


--

set foreign_key_checks=1;
