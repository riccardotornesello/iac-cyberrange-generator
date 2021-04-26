CREATE DATABASE IF NOT EXISTS admin_console;
USE admin_console;

GRANT SELECT ON admin_console.* TO 'challengeuser'@'%' IDENTIFIED BY '3b8743o4bf';

CREATE TABLE IF NOT EXISTS users
(
  username VARCHAR(64) PRIMARY KEY,
  password VARCHAR(64) NOT NULL
);

INSERT IGNORE INTO users
  (username, password)
VALUES
  ('I_4m_y0ur_b0ss', 'nFD1w#YbJ$gR');