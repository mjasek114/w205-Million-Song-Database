USE metamusic

LOAD DATA LOCAL INFILE '/tmp/Song.csv'
INTO TABLE song
FIELDS 
  TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  ESCAPED BY '\\'
(@artist, @title, @writer, @songYear, @peakPosition, 
 @billboardYear, @artistHotttness, @songHotttness,
 @songKey, @tempo, @duration, @loudness,
 @timeSignature, @mode)
SET
  artist = nullif(@artist, ''),
  title = nullif(@title, ''),
  writer = nullif(@writer, ''),
  songYear = nullif(@songYear, ''),
  peakPosition = nullif(@peakPosition, ''),
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
