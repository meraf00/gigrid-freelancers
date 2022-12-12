DROP DATABASE IF EXISTS FreelancePlatform;

CREATE DATABASE FreelancePlatform;

USE FreelancePlatform;


CREATE TABLE User(
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    `password` VARCHAR(300) NOT NULL,
    date_of_birth DATETIME NOT NULL,
    user_type ENUM('FREELANCER', 'EMPLOYER'),
    token VARCHAR(200)
);


CREATE TABLE Chat(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_1 INT NOT NULL, -- chat initiator
    user_2 INT NOT NULL,

    FOREIGN KEY (user_1) REFERENCES User(id),
    FOREIGN KEY (user_2) REFERENCES User(id)
);

CREATE TABLE `Message`(
    id INT AUTO_INCREMENT,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    time_stamp DATETIME NOT NULL DEFAULT NOW(),

    content_type ENUM('TEXT', 'FILE') default 'TEXT',
    content VARCHAR(4000) NOT NULL,

    FOREIGN KEY (chat_id) REFERENCES Chat(id),
    FOREIGN KEY (sender_id) REFERENCES User(id),
    PRIMARY KEY (id, chat_id)    
);

CREATE TABLE `File`(
    id CHAR(36) PRIMARY KEY,
    file_name VARCHAR(30),
    file_path VARCHAR(260),
    mime_type VARCHAR(128) 
);

-- CREATE TABLE `Attachment`(
--     id INT PRIMARY KEY,
--     file_id VARCHAR(36),

--     FOREIGN KEY (file_id) REFERENCES `File`(id)
-- );