DROP TABLE IF EXISTS link;

CREATE TABLE link (
  id VARCHAR(6) PRIMARY KEY,
  link TEXT NOT NULL,
  clicks SMALLINT DEFAULT 0
);