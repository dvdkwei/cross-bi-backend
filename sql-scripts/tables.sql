ALTER TABLE IF EXISTS cb_user_workspace DROP CONSTRAINT pk_cb_user_workspace;
DROP TABLE IF EXISTS cb_user_workspace;
DROP TABLE IF EXISTS cb_password CASCADE;
ALTER TABLE IF EXISTS cb_user DROP CONSTRAINT fk_password;
DROP TABLE IF EXISTS cb_user;
DROP TABLE IF EXISTS cb_workspace;

CREATE TABLE cb_password (
  password_id SERIAL PRIMARY KEY,
  current_value VARCHAR(50) NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cb_workspace (
  workspace_id SERIAL PRIMARY KEY
);

CREATE TABLE cb_user (
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(50) NOT NULL,
  forename VARCHAR(75) NOT NULL,
  surname VARCHAR(50) NOT NULL,
  company VARCHAR(50),
  password_id INTEGER, 
  CONSTRAINT fk_password 
    FOREIGN KEY(password_id)
      REFERENCES cb_password(password_id) 
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE cb_user_workspace (
  workspace_id INT REFERENCES cb_workspace(workspace_id) ON UPDATE CASCADE ON DELETE CASCADE,
  user_id INT REFERENCES cb_user(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT pk_cb_user_workspace PRIMARY KEY (workspace_id, user_id)
);

