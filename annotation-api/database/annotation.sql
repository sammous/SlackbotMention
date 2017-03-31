CREATE DATABASE Annotations DEFAULT CHARACTER SET utf8;
USE Annotations;
CREATE TABLE `Annotations` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `mention_id` bigint(20) NOT NULL,
        `alert_id` int(11) DEFAULT NULL,
        `text` varchar(255),
        `count_neutral` int(11) DEFAULT 0,
        `count_neg` int(11) DEFAULT 0,
        `count_pos` int(11) DEFAULT 0,
        `count_idk` int(11) DEFAULT 0,
        `sourceUrl` varchar(500) DEFAULT NULL,
        PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
CREATE TABLE `Score` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(255),
        `score` int(11) DEFAULT 0,
        PRIMARY KEY(`id`),
        UNIQUE KEY `username` (`name`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
