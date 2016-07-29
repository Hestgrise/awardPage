CREATE TABLE users (
id INT AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
dateCreated DATETIME NOT NULL,
signature VARCHAR(255) NOT NULL,
PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE admins (
id INT AUTO_INCREMENT,
email VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
dateCreated DATETIME NOT NULL,
PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE awards (
id INT AUTO_INCREMENT,
userId INT NOT NULL,
type VARCHAR(255) NOT NULL,
awardee VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
dateAwarded DATETIME NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (userId) REFERENCES users(id)
) ENGINE = InnoDB;