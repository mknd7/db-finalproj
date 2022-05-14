CREATE TABLE User (
  userid INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  email VARCHAR(64) NOT NULL,
  password CHAR(32) NOT NULL, -- password is hashed using MD5()
  profile TEXT(140),
  status VARCHAR(20) NOT NULL DEFAULT 'beginner',
  addr_city VARCHAR(45),
  addr_state VARCHAR(45),
  addr_country VARCHAR(45),
  PRIMARY KEY (userid),
  UNIQUE (username),
  UNIQUE (email),
  CHECK (status IN ('beginner', 'intermediate', 'advanced', 'expert'))
);

CREATE TABLE Topic (
  topicid INT NOT NULL,
  topicname VARCHAR(45) NOT NULL,
  PRIMARY KEY (topicid),
  UNIQUE (topicname)
);

CREATE TABLE TopicInner (
  tinnerid INT NOT NULL,
  topicid INT NOT NULL,
  topicname VARCHAR(45) NOT NULL,
  PRIMARY KEY (tinnerid),
  FOREIGN KEY (topicid) REFERENCES Topic (topicid)
);

CREATE TABLE Question (
  qnid INT NOT NULL AUTO_INCREMENT,
  userid INT NOT NULL,
  topicid INT NOT NULL,
  qnwhen DATETIME,
  title VARCHAR(140) NOT NULL,
  qnbody TEXT(256) NOT NULL,
  resolved BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (qnid),
  FOREIGN KEY (userid) REFERENCES User (userid),
  FOREIGN KEY (topicid) REFERENCES Topic (topicid)
);

CREATE TABLE Answer (
  ansid INT NOT NULL AUTO_INCREMENT,
  qnid INT NOT NULL,
  userid INT NOT NULL,
  answhen DATETIME,
  ansbody TEXT(256) NOT NULL,
  best BOOLEAN NOT NULL DEFAULT false,
  upvotes INT DEFAULT 0,
  PRIMARY KEY (ansid),
  FOREIGN KEY (qnid) REFERENCES Question (qnid),
  FOREIGN KEY (userid) REFERENCES User (userid)
);
