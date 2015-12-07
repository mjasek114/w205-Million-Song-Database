USE metamusic;

CREATE INDEX IX_song_artist_title
ON song (artist);

CREATE INDEX IX_song_writer_title
ON song(writer);
