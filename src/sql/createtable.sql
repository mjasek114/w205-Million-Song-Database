USE metamusic

CREATE TABLE song (
	artist VARCHAR(256),
	title VARCHAR(1024),
	writer VARCHAR(256),
	songYear INT,
	peakPosition INT,
	billboardYear INT,
	artistHotttness FLOAT,
	songHotttness FLOAT,
	danceability FLOAT,
	songKey VARCHAR(10),
	tempo FLOAT,
	duration FLOAT,
	loudness FLOAT,
	timeSignature INT
);