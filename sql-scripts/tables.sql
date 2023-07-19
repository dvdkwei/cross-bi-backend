ALTER TABLE IF EXISTS cb_user_workspace DROP CONSTRAINT pk_cb_user_workspace;
DROP TABLE IF EXISTS cb_user_workspace;
DROP TABLE IF EXISTS cb_password CASCADE;
ALTER TABLE IF EXISTS cb_user DROP CONSTRAINT fk_password;
DROP TABLE IF EXISTS cb_user;
DROP TABLE IF EXISTS cb_workspace;

CREATE TABLE cb_password (
  id SERIAL PRIMARY KEY,
  current_value VARCHAR(100) NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cb_workspace (
  id SERIAL PRIMARY KEY
);

CREATE TABLE cb_user (
  id SERIAL PRIMARY KEY,
  email VARCHAR(100) NOT NULL,
  forename VARCHAR(100) NOT NULL,
  surname VARCHAR(75) NOT NULL,
  company VARCHAR(50),
  password_id INTEGER, 
  CONSTRAINT fk_password 
    FOREIGN KEY(password_id)
      REFERENCES cb_password(id) 
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE cb_user_workspace (
  workspace_id INT REFERENCES cb_workspace(id) ON UPDATE CASCADE ON DELETE CASCADE,
  user_id INT REFERENCES cb_user(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT pk_cb_user_workspace PRIMARY KEY (workspace_id, user_id)
);

