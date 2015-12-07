CREATE INDEX IX_song_artist_title
ON song (artist, title);

CREATE INDEX IX_song_writer_title
ON song(writer, title);

CREATE INDEX IX_song_title
ON song(title);

CREATE INDEX IX_song_songYear
ON song(songYear);

CREATE INDEX IX_song_peakPosition
ON song(peakPosition);

CREATE INDEX IX_song_billboardYear
ON song(billboardYear);

CREATE INDEX IX_song_artistHotttness
ON song(artistHotttness);

CREATE INDEX IX_song_songHotttness
ON song(songHotttness);
