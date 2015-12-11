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
	key STRING,
	tempo STRING,
	duration STRING,
	loudness STRING,
	timeSignature STRING,
	mode STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION 's3://w205-mmm/merged';

INSERT OVERWRITE TABLE merged 
SELECT 
	CASE WHEN m.artist_name = '' OR m.artist_name = 'NA' THEN NULL ELSE m.artist_name END,
	CASE WHEN m.title = '' OR m.title = 'NA' THEN NULL ELSE m.title END,
	CASE WHEN a.Name = '' OR a.Name = 'NA' THEN NULL ELSE a.Name END AS writer,
	CASE WHEN m.year = '' OR m.year = 'NA' OR m.year = '0' THEN NULL ELSE m.year END,
	CASE WHEN b.Peak = '' OR b.Peak = 'NA' OR b.Peak = '0' THEN NULL ELSE b.Peak END,
	CASE WHEN b.Year = '' OR b.Year = 'NA' OR b.year = '0' THEN NULL ELSE b.Year END AS billboardYear,
	CASE WHEN m.artist_hotttnesss = '' OR m.artist_hotttnesss = 'NA' OR m.artist_hotttnesss = '0' THEN NULL ELSE m.artist_hotttnesss END,
	CASE WHEN m.song_hotttnesss = '' OR m.song_hotttnesss = 'NA' OR m.song_hotttnesss = '0' THEN NULL ELSE m.song_hotttnesss END,
	CASE WHEN k.Name = '' OR k.Name = 'NA' THEN NULL ELSE k.Name END AS key,
	CASE WHEN m.tempo = '' OR m.tempo = 'NA' OR m.tempo = '0' THEN NULL ELSE m.tempo END,
	CASE WHEN m.duration = '' OR m.duration = 'NA' OR m.duration = '0' THEN NULL ELSE m.duration END,
	CASE WHEN m.loudness = '' OR m.loudness = 'NA' OR m.loudness = '0' THEN NULL ELSE m.loudness END,
	CASE WHEN m.time_signature = '' OR m.time_signature = 'NA' OR m.time_signature = '0' THEN NULL ELSE m.time_signature END,
	CASE WHEN m.mode = '0' THEN 'minor'
         WHEN m.mode = '1' THEN 'major' 
         ELSE NULL END
FROM msd m
LEFT JOIN ascap a
	ON a.Title = m.title
LEFT JOIN billboard b
	ON b.Title = m.title
	AND b.artist = m.artist_name
LEFT JOIN key k
	ON k.id = m.key;
