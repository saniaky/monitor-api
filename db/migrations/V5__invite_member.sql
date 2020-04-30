-- Invite new members to a project
CREATE TABLE `project_invite`
(
    `invite_id`  bigint                  NOT NULL AUTO_INCREMENT,
    `sender_id`  bigint                  NOT NULL,
    `project_id` bigint                  NOT NULL,
    `role`       enum ('ADMIN','MEMBER') NOT NULL,
    `email`      varchar(45)             NOT NULL,
    `token`      varchar(45)             NOT NULL,
    `created_at` datetime                NOT NULL DEFAULT NOW(),
    `message`    varchar(512)            NULL,

    PRIMARY KEY (`invite_id`),
    CONSTRAINT `fk_project_invites_sender_id` FOREIGN KEY (`sender_id`)
        REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_project_invites_project_id` FOREIGN KEY (`project_id`)
        REFERENCES `project` (`project_id`) ON DELETE CASCADE
);

