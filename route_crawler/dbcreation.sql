DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS location;

CREATE TABLE IF NOT EXISTS `location` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255),
    `longitude` decimal(12, 8),
    `latitude` decimal(12, 8),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `schedule` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `route` varchar(255) NOT NULL,
    `start_loc_id` int(11) NOT NULL,
    `end_loc_id` int(11) NOT NULL,
    `start_time` datetime,
    `end_time` datetime,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
