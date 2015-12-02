CREATE EXTERNAL TABLE ascap (
	Title STRING,
	RoleType STRING,
	Name STRING,
	Shares INT,
	Note STRING
	)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://w205-mmm/ascap'
tblproperties ("skip.header.line.count"="1");

CREATE TABLE ascap_writers (
	Title STRING,
	Name STRING,
	Shares INT,
	Note STRING
	)
STORED AS ORC;

INSERT INTO ascap_writers (
	Title, RoleType, Name, Shares, Note
	)
SELECT 
	Title, 
	regexp_replace(Name, '(\\w+)\\s(.+)', '$2 $1'),
	Shares,
	Note
FROM ascap
WHERE RoleType = 'W';