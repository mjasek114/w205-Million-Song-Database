USE metamusic;

CREATE INDEX IX_song_artist
ON song (artist);

CREATE INDEX IX_song_writer
ON song_writer (writer);
