CREATE EXTERNAL TABLE billboard (
	Artist STRING,
	Title STRING,
	High INT,
	Year STRING
	)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION 's3://w205-mmm/billboard';