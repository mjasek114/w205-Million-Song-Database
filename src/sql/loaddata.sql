USE metamusic

LOAD DATA LOCAL INFILE '/tmp/Song.csv'
INTO TABLE song
FIELDS 
  TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  ESCAPED BY '\\'
(@artist, @title, @writer, @songYear, @peakPosition, 
 @billboardYear, @artistHotttness, @songHotttness,
 @danceability, @songKey, @tempo, @duration, @loudness,
 @timeSignature, @energy, @mode)
SET
  artist = nullif(@artist, ''),
  title = nullif(@title, ''),
  writer = nullif(@writer, ''),
  songYear = nullif(@songYear, ''),
  peakPosition = nullif(@peakPosition, ''),
  billboardYear = nullif(@billboardYear, ''),
  artistHotttness = nullif(@artistHotttness, ''),
  songHotttness = nullif(@songHotttness, ''),
  danceability = nullif(@danceability, ''),
  songKey = nullif(@songKey, ''),
  tempo = nullif(@tempo, ''),
  duration = nullif(@duration, ''),
  loudness = nullif(@loudness, ''),
  timeSignature = nullif(@timeSignature, ''),
  energy = nullif(@energy, ''),
  mode = nullif(@mode, '')
;
