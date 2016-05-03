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

INSERT OVERWRITE TABLE billboard
SELECT 
	regexp_replace(Artist, '"(\\w+), The"', 'The $1'),
	Title,
	Peak,
	Year
FROM billboard_staging;
