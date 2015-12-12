#!/bin/bash

mysql < ./createdb.sql
mysql < ./createuser.sql

mkdir -p /tmp/songs
aws s3 sync s3://w205-mmm/merged /tmp/songs
cat /tmp/songs/* > /tmp/Song.csv

mysql < ./create_song_table.sql
mysql < ./load_song_data.sql
mysql < ./create_song_index.sql

#mkdir -p /tmp/writers
#aws s3 sync s3://w205-mmm/writers /tmp/writers
#cat /tmp/writers/* > /tmp/Writer.csv

#mysql < ./create_writer_table.sql
#mysql < ./load_writer_data.sql
#mysql < ./create_writer_index.sql

