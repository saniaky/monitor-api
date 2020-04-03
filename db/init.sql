DROP DATABASE IF EXISTS `monitor`;
DROP USER IF EXISTS 'monitor_api'@'%';

CREATE DATABASE `monitor`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

CREATE USER 'monitor_api'@'%' IDENTIFIED WITH mysql_native_password BY 'ChangeMe';
GRANT ALL PRIVILEGES ON `monitor`.* TO 'monitor_api'@'%';
FLUSH PRIVILEGES;
