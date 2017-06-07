CREATE TABLE key_entries (
  db INT DEFAULT 0,
  skey VARCHAR,
  id SERIAL UNIQUE,
  key_type INT,
  PRIMARY KEY(db, skey)
);

CREATE TABLE global_hashmap (
  id INT PRIMARY KEY REFERENCES key_entries(id) ON DELETE CASCADE,
  value TEXT,
  expiration_date TIMESTAMP
);

CREATE TABLE hashmap (
  id INT REFERENCES key_entries(id) ON DELETE CASCADE,
  hkey VARCHAR,
  value TEXT,
  PRIMARY KEY(id, hkey)
);

CREATE TABLE set_element_lookup (
  db INT DEFAULT 0,
  skey VARCHAR,
  id SERIAL,
  PRIMARY KEY(db, skey)
);

CREATE INDEX ON set_element_lookup(id);

CREATE TABLE set_hashmap (
  id INT PRIMARY KEY REFERENCES key_entries(id) ON DELETE CASCADE,
  elements INT[]
);