-- log actions
CREATE TABLE `audit_log`
(
    `event_id`   bigint      NOT NULL AUTO_INCREMENT,
    `project_id` bigint      NOT NULL,
    `user_id`    bigint      NULL, -- NULL - in case if user will be deleted
    `user_ip`    varchar(10) NULL,
    `time`       datetime    NOT NULL DEFAULT NOW(),
    `action`     varchar(45) NOT NULL,

    PRIMARY KEY (`event_id`),
    CONSTRAINT `fk_audit_log_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE CASCADE
);

