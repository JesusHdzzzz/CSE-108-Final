ALTER TABLE user_web RENAME TO user_web_backup;

CREATE TABLE `user_web` (
    user_id INT,
    website_id INT,
    PRIMARY KEY (user_id, website_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(website_id) REFERENCES Web(website_id) ON DELETE CASCADE
);

INSERT INTO user_web (user_id, website_id)
SELECT user_id, website_id FROM user_web_backup;

DROP TABLE user_web_backup;