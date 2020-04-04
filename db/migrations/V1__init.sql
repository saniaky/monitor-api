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
    `password_age`             datetime     NULL     DEFAULT NOW(),
    `avatar_url`               varchar(256) NULL,
    `failed_login_attempts`    tinyint      NULL,
    `last_login`               datetime     NULL,
    `is_active`                bit          NOT NULL DEFAULT 1,
    `is_admin`                 bit          NOT NULL DEFAULT 0,
    `created_at`               datetime     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (`user_id`),
    UNIQUE KEY `email_unique` (`email`)
);
