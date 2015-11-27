CREATE EXTERNAL TABLE billboard_staging (
	Artist STRING,
	Title STRING,
	Peak INT,
	Year STRING
	)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION 's3://w205-mmm/billboard'
tblproperties ("skip.header.line.count"="1");

CREATE TABLE billboard (
	Artist STRING,
	Title STRING,
	Peak INT,
	Year STRING
	)
STORED AS ORC;

INSERT INTO billboard (
	Artist, Title, High, Peak)
SELECT 
	regexp_replace(Artist, "\"(\\w+), The\"", "The $1"),
	Title,
	High,
	Year
	)
FROM billboard_staging;
