
/* CREATE STATEMENTS FOR PYTHON WEBSERVICE TESTER */
CREATE DATABASE `ci_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_name` varchar(45) DEFAULT NULL,
  `service_name` varchar(45) DEFAULT NULL,
  `operation_name` varchar(45) DEFAULT NULL,
  `case_id` int(11) DEFAULT NULL,
  `response` longtext,
  `result` varchar(22) DEFAULT NULL,
  `diff` longtext,
  `build_num` varchar(45) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1124 DEFAULT CHARSET=utf8;
CREATE TABLE `systems` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `host` varchar(45) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `env` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `test_cases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) DEFAULT NULL,
  `service_name` varchar(45) DEFAULT NULL,
  `operation_name` varchar(45) DEFAULT NULL,
  `uri` longtext,
  `request_body` longtext,
  `desired_response` longtext,
  `response_type` varchar(45) DEFAULT NULL,
  `provider_operation_id` int(11) DEFAULT NULL,
  `version` varchar(45) DEFAULT NULL,
  `response_ignore` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8;
