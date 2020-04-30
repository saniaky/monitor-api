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
    `email_verified`           bool         NOT NULL DEFAULT 1,
    `email_verification_token` varchar(45)  NULL,
    `password`                 varchar(60)  NOT NULL,
    `password_reset_token`     varchar(45)  NULL,
    `password_reset_expires`   datetime     NULL,
    `password_age`             datetime     NOT NULL DEFAULT NOW(),
    `avatar_url`               varchar(256) NULL,
    `country_id`               char(2)      NULL,
    `failed_login_attempts`    tinyint      NULL,
    `last_login`               datetime     NULL,
    `is_active`                bool         NOT NULL DEFAULT 1,
    `is_admin`                 bool         NOT NULL DEFAULT 0,
    `created_at`               datetime     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (`user_id`),
    UNIQUE KEY `user_email_unique` (`email`),
    CONSTRAINT `fk_user_country` FOREIGN KEY (`country_id`)
        REFERENCES `country` (`iso2`) ON DELETE RESTRICT
);


CREATE TABLE `project`
(
    `project_id` bigint      NOT NULL AUTO_INCREMENT,
    `name`       varchar(45) NOT NULL,
    `created_at` datetime    NOT NULL DEFAULT NOW(),

    PRIMARY KEY (`project_id`)
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


CREATE TABLE `incident`
(
    `incident_id` bigint                  NOT NULL AUTO_INCREMENT,
    `project_id`  bigint                  NOT NULL,
    `author_id`   bigint                  NOT NULL,
    `name`        varchar(45)             NOT NULL,
    `status`      enum ('OPEN', 'CLOSED') NOT NULL DEFAULT 'OPEN',
    `components`  varchar(45)             NULL,

    PRIMARY KEY (`incident_id`),
    CONSTRAINT `fk_incident_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_incident_author_id` FOREIGN KEY (`author_id`)
        REFERENCES `user` (`user_id`) ON DELETE RESTRICT
);


CREATE TABLE `incident_update`
(
    `update_id`   bigint                                                      NOT NULL AUTO_INCREMENT,
    `incident_id` bigint                                                      NOT NULL,
    `message`     varchar(512)                                                NOT NULL,
    `status`      enum ('INVESTIGATING','IDENTIFIED','MONITORING','RESOLVED') NOT NULL,
    `created_at`  datetime                                                    NOT NULL,

    PRIMARY KEY (`update_id`),
    CONSTRAINT `fk_incident_update_id` FOREIGN KEY (`incident_id`)
        REFERENCES `incident` (`incident_id`) ON DELETE CASCADE
);

