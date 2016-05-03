-- Using strings for all fields b/c output is a CSV.
-- I'm not sure there's much value in worrying about
-- types up to this point if type info is being 
-- discarded.
CREATE EXTERNAL TABLE msd (
	mode_confidence STRING,
	idx_tatums_start STRING,
	key_confidence STRING,
	energy STRING,
	idx_segments_loudness_max STRING,
	idx_beats_confidence STRING,
	idx_segments_pitches STRING,
	release_7digitalid STRING,
	year STRING,
	duration STRING,
	artist_mbid STRING,
	artist_7digitalid STRING,
	idx_artist_terms STRING,
	end_of_fade_in STRING,
	time_signature_confidence STRING,
	artist_longitude STRING,
	idx_segments_loudness_max_time STRING,
	idx_sections_start STRING,
	artist_playmeid STRING,
	track_id STRING,
	artist_latitude STRING,
	danceability STRING,
	idx_segments_loudness_start STRING,
	idx_sections_confidence STRING,
	artist_familiarity STRING,
	artist_id STRING,
	start_of_fade_out STRING,
	idx_tatums_confidence STRING,
	analysis_sample_rate STRING,
	idx_bars_start STRING,
	idx_bars_confidence STRING,
	idx_segments_timbre STRING,
	song_hotttnesss STRING,
	tempo STRING,
	artist_name STRING,
	idx_segments_start STRING,
	artist_hotttnesss STRING,
	idx_beats_start STRING,
	key STRING,
	genre STRING,
	audio_md5 STRING,
	track_7digitalid STRING,
	artist_location STRING,
	song_id STRING,
	title STRING,
	idx_similar_artists STRING,
	idx_segments_confidence STRING,
	analyzer_version STRING,
	mode STRING,
	time_signature STRING,
	release STRING,
	loudness STRING,
	idx_artist_mbtags STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION 's3://w205-mmm/million_song_dataset'
tblproperties ("skip.header.line.count"="1");