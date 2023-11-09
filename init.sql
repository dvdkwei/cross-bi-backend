DROP TABLE IF EXISTS cb_incident CASCADE;
DROP TABLE IF EXISTS cb_view CASCADE;
DROP TABLE IF EXISTS cb_diagramm_type CASCADE;
DROP TABLE IF EXISTS cb_dashboard CASCADE;
DROP TABLE IF EXISTS cb_user_workspace CASCADE;
DROP TABLE IF EXISTS cb_password CASCADE;
DROP TABLE IF EXISTS cb_user CASCADE;
DROP TABLE IF EXISTS cb_workspace CASCADE;

CREATE TABLE cb_password (
  id SERIAL PRIMARY KEY,
  current_value VARCHAR(100) NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cb_workspace (
  id SERIAL PRIMARY KEY,
  name VARCHAR
);

CREATE TABLE cb_user (
  id SERIAL PRIMARY KEY,
  email VARCHAR(100) NOT NULL,
  forename VARCHAR(100) NOT NULL,
  surname VARCHAR(75) NOT NULL,
  company VARCHAR(50),
  username VARCHAR(100),
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

CREATE TABLE cb_dashboard (
	id SERIAL PRIMARY KEY,
	name VARCHAR(150) NOT NULL,
	updated_at DATE DEFAULT CURRENT_DATE,
  workspace_id INTEGER,
  CONSTRAINT fk_workspace 
    FOREIGN KEY(workspace_id)
      REFERENCES cb_workspace(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE cb_diagramm_type (
  id INTEGER PRIMARY KEY,
  name VARCHAR
);

INSERT INTO cb_diagramm_type (id, name) 
VALUES 
  (1, 'Big Number'), 
  (2, 'Bar'),
  (3, 'Line'),
  (4, 'Donut'),
  (5, 'List'),
  (6, 'Map')

CREATE TABLE cb_view (
	id SERIAL PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	updated_at DATE DEFAULT CURRENT_DATE,
  dashboard_id INTEGER,
  workspace_id INTEGER,
  diagramm_type INTEGER,
  x_axis VARCHAR,
  y_axis VARCHAR,
  aggregate VARCHAR(10),
  categories VARCHAR,
  title VARCHAR(50),
  date_column VARCHAR,
  CONSTRAINT fk_dashboard 
    FOREIGN KEY(dashboard_id)
      REFERENCES cb_dashboard(id)
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_workspace
    FOREIGN KEY(workspace_id)
      REFERENCES cb_workspace(id)
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_dtype
    FOREIGN KEY(diagramm_type)
      REFERENCES cb_diagramm_type(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE cb_incident (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  description VARCHAR,
  department VARCHAR(50),
  status INTEGER DEFAULT 0
);

CREATE TABLE cb_pushsubscription (
  id SERIAL PRIMARY KEY,
  subscription_json VARCHAR
);