CREATE TABLE IF NOT EXISTS `route` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `number` smallint(5),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `bus_stop` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255),
    `longitude` decimal(12, 8),
    `latitude` decimal(12, 8),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `schedule` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `route_id` int(11) NOT NULL,
    `bs_start_id` int(11) NOT NULL,
    `bs_end_id` int(11) NOT NULL,
    `start_time` datetime,
    `end_time` datetime,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `location` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `uid` varchar(50),
    `code` varchar(10),
    `name` varchar(255) DEFAULT NULL,
    `latitude` decimal(12,8) DEFAULT NULL,
    `longitude` decimal(12,8) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_uid` (`uid`),
    UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `route` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `uid` varchar(50),
    `name` varchar(255) NOT NULL,
    `short_name` varchar(15) NOT NULL,
    `description` varchar(255),
    `url` varchar(255) DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

