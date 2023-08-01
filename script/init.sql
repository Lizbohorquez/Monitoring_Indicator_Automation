-- Drop existing tables if they exist to avoid conflicts during initialization
DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS score;
DROP TABLE IF EXISTS organization;
DROP TABLE IF EXISTS aws_account;

-- Create the "aws_account" table
CREATE TABLE IF NOT EXISTS aws_account(
id INT UNIQUE NOT NULL,
name VARCHAR(50) NOT NULL,
environment VARCHAR(50),
organization VARCHAR(50),
PRIMARY KEY(id)
);

-- Create the "organization" table
CREATE TABLE IF NOT EXISTS organization(
id INT NOT NULL,
aws_account_id INT NOT NULL UNIQUE,
grafana_folder VARCHAR(255) NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (aws_account_id) REFERENCES aws_account(id)
);

-- Create the "service" table
CREATE TABLE IF NOT EXISTS service(
id INT NOT NULL,
organization_id INT NOT NULL,
name VARCHAR(50) NOT NULL,
type VARCHAR(50),
monitored VARCHAR(50),
PRIMARY KEY (id),
FOREIGN KEY (organization_id) REFERENCES organization(id)
);

-- Create the "score" table
CREATE TABLE IF NOT EXISTS score(
id INT NOT NULL,
organization_id INT NOT NULL,
infrastructure_monitoring INT,
proactive_monitoring INT,
realtime_monitoring INT,
total INT,
PRIMARY KEY (id),
FOREIGN KEY (organization_id) REFERENCES organization(id),
CONSTRAINT infrastructure_monitoring_ck CHECK (infrastructure_monitoring BETWEEN 0 AND 100),
CONSTRAINT proactive_monitoring_ck CHECK (proactive_monitoring BETWEEN 0 AND 100),
CONSTRAINT realtime_monitoring_ck CHECK (realtime_monitoring BETWEEN 0 AND 100)
);