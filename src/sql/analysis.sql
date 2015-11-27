-- Using strings for all fields b/c output is a CSV.
-- I'm not sure there's much value in worrying about
-- types up to this point if type info is being 
-- discarded.
CREATE EXTERNAL TABLE merged (
	artist STRING,
	title STRING,
	writer STRING,
	year STRING,
	peakPosition STRING,
	billboardYear STRING,
	artistHotttness STRING,
	songHotttness STRING,
	danceability STRING,
	key STRING,
	tempo STRING,
	duration STRING,
	loudness STRING,
	timeSignature STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION 's3://w205-mmm/merged';

INSERT INTO TABLE merged 
SELECT 
	m.artist_name,
	m.title,
	a.Name AS writer,
	m.year,
	b.Peak,
	b.Year AS billboardYear,
	m.artist_hotttnesss,
	m.song_hotttnesss,
	m.danceability,
	k.Name AS key,
	m.tempo,
	m.duration,
	m.loudness,
	m.time_signature
FROM msd m
LEFT JOIN ascap a
	ON a.Title = m.title
LEFT JOIN billboard b
	ON b.Title = m.title
	AND b.artist = m.artist_name
LEFT JOIN key k
	ON k.id = m.key;
