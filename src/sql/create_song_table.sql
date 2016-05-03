USE metamusic

CREATE TABLE song (
	artist VARCHAR(256),
	title VARCHAR(500),
	songYear INT,
	peakPosition INT,
	billboardYear INT,
	artistHotttness FLOAT,
	songHotttness FLOAT,
	songKey VARCHAR(10),
	tempo FLOAT,
	duration FLOAT,
	loudness FLOAT,
	timeSignature INT,
	mode VARCHAR(10)
);
