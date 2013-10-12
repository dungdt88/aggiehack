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
