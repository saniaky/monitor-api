CREATE TABLE `country`
(
    `iso2` char(2)     NOT NULL,
    `iso3` char(3)     NOT NULL,
    `name` varchar(45) NOT NULL,

    PRIMARY KEY (`iso2`),
    UNIQUE KEY `country_iso2_unique` (`iso2`),
    UNIQUE KEY `country_iso3_unique` (`iso3`),
    UNIQUE KEY `country_name_unique` (`name`)
);


CREATE TABLE `user`
(
    `user_id`                  bigint       NOT NULL AUTO_INCREMENT,
    `first_name`               varchar(45)  NOT NULL,
    `last_name`                varchar(45)  NOT NULL,
    `email`                    varchar(45)  NOT NULL,
    `email_verified`           bit          NOT NULL DEFAULT 1,
    `email_verification_token` varchar(45)  NULL,
    `password`                 varchar(60)  NOT NULL,
    `password_reset_token`     varchar(45)  NULL,
    `password_reset_expires`   datetime     NULL,
    `password_age`             datetime     NOT NULL DEFAULT NOW(),
    `avatar_url`               varchar(256) NULL,
    `country_id`               char(2)      NULL,
    `failed_login_attempts`    tinyint      NULL,
    `last_login`               datetime     NULL,
    `is_active`                bit          NOT NULL DEFAULT 1,
    `is_admin`                 bit          NOT NULL DEFAULT 0,
    `created_at`               datetime     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (`user_id`),
    UNIQUE KEY `user_email_unique` (`email`),
    CONSTRAINT `fk_user_country` FOREIGN KEY (`country_id`)
        REFERENCES `country` (`iso2`) ON DELETE RESTRICT
);


CREATE TABLE `project`
(
    `project_id` bigint      NOT NULL AUTO_INCREMENT,
    `name`       varchar(15) NOT NULL,

    PRIMARY KEY (`project_id`)
);


CREATE TABLE `audit_log`
(
    `event_id`   bigint      NOT NULL AUTO_INCREMENT,
    `project_id` bigint      NOT NULL,
    `user_id`    bigint      NOT NULL, -- NULL - in case if user will be deleted
    `user_ip`    varchar(10) NOT NULL,
    `time`       datetime    NOT NULL,
    `action`     varchar(45) NOT NULL,

    PRIMARY KEY (`event_id`),
    CONSTRAINT `fk_audit_log_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE CASCADE
);


CREATE TABLE `user_project`
(
    `user_id`    bigint                  NOT NULL,
    `project_id` bigint                  NOT NULL,
    `role`       enum ('ADMIN','MEMBER') NOT NULL DEFAULT 'MEMBER',

    CONSTRAINT `fk_project_team_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_project_team_user_id` FOREIGN KEY (`user_id`)
        REFERENCES `user` (`user_id`) ON DELETE CASCADE
);


CREATE TABLE `app`
(
    `app_id`            bigint       NOT NULL AUTO_INCREMENT,
    `project_id`        bigint       NOT NULL,
    `name`              varchar(45)  NOT NULL,
    `checks_per_minute` int          NOT NULL,
    `current_url`       varchar(512) NOT NULL,

    PRIMARY KEY (`app_id`),
    CONSTRAINT `fk_app_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE RESTRICT
);


CREATE TABLE `maintenance`
(
    `maintenance_id` bigint       NOT NULL AUTO_INCREMENT,
    `app_id`         bigint       NOT NULL,
    `schedule`       datetime     NOT NULL,
    `description`    varchar(512) NOT NULL,

    PRIMARY KEY (`maintenance_id`),
    CONSTRAINT `fk_maintenance_app_id` FOREIGN KEY (`app_id`)
        REFERENCES `app` (`app_id`) ON DELETE CASCADE
);


CREATE TABLE `incident`
(
    `incident_id` bigint      NOT NULL AUTO_INCREMENT,
    `app_id`      bigint      NOT NULL,
    `author_id`   bigint      NOT NULL,
    `title`       varchar(45) NOT NULL,
    `time`        datetime    NOT NULL,
    `components`  varchar(45) NULL,

    PRIMARY KEY (`incident_id`),
    CONSTRAINT `fk_incident_app_id` FOREIGN KEY (`app_id`)
        REFERENCES `app` (`app_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_incident_author_id` FOREIGN KEY (`author_id`)
        REFERENCES `user` (`user_id`) ON DELETE RESTRICT
);


CREATE TABLE `incident_update`
(
    `update_id`   bigint                                                      NOT NULL AUTO_INCREMENT,
    `incident_id` bigint                                                      NOT NULL,
    `status`      enum ('INVESTIGATING','IDENTIFIED','MONITORING','RESOLVED') NOT NULL,
    `created_at`  datetime                                                    NOT NULL,

    PRIMARY KEY (`update_id`),
    CONSTRAINT `fk_incident_update_id` FOREIGN KEY (`incident_id`)
        REFERENCES `incident` (`incident_id`) ON DELETE CASCADE
);

