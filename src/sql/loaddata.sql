USE metamusic

LOAD DATA LOCAL INFILE '/tmp/Song.csv'
INTO TABLE song
FIELDS 
  TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  ESCAPED BY '\\'
(@artist, @title, @songYear, @peakPosition, 
 @billboardYear, @artistHotttness, @songHotttness,
 @songKey, @tempo, @duration, @loudness,
 @timeSignature, @mode)
SET
  artist = nullif(@artist, ''),
  title = nullif(@title, ''),
  songYear = nullif(@songYear, ''),
  peakPosition = nullif(nullif(@peakPosition, ''), '0'),
  billboardYear = nullif(@billboardYear, ''),
  artistHotttness = nullif(@artistHotttness, ''),
  songHotttness = nullif(@songHotttness, ''),
  songKey = nullif(@songKey, ''),
  tempo = nullif(@tempo, ''),
  duration = nullif(@duration, ''),
  loudness = nullif(@loudness, ''),
  timeSignature = nullif(@timeSignature, ''),
  mode = nullif(@mode, '')
;

UPDATE song SET artistHotttness = NULL WHERE artistHotttness = 0;
UPDATE song SET songHotttness = NULL WHERE songHotttness = 0;



LOAD DATA LOCAL INFILE '/tmp/Writer.csv'
INTO TABLE song_writer
FIELDS 
  TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  ESCAPED BY '\\'
( @title, @writer, @songYear, @peakPosition, 
 @billboardYear, @artistHotttness, @songHotttness,
 @songKey, @tempo, @duration, @loudness,
 @timeSignature, @mode)
SET
  title = nullif(@title, ''),
  writer = nullif(@writer, ''),
  songYear = nullif(@songYear, ''),
  peakPosition = nullif(nullif(@peakPosition, ''), '0'),
  billboardYear = nullif(@billboardYear, ''),
  artistHotttness = nullif(@artistHotttness, ''),
  songHotttness = nullif(@songHotttness, ''),
  songKey = nullif(@songKey, ''),
  tempo = nullif(@tempo, ''),
  duration = nullif(@duration, ''),
  loudness = nullif(@loudness, ''),
  timeSignature = nullif(@timeSignature, ''),
  mode = nullif(@mode, '')
;

UPDATE song_writer SET artistHotttness = NULL WHERE artistHotttness = 0;
UPDATE song_writer SET songHotttness = NULL WHERE songHotttness = 0;