#!/bin/bash

mkdir -p /tmp/songs
aws s3 sync s3://w205-mmm/merged /tmp/songs

cat /tmp/songs/* > /tmp/Song.csv

mysql < ./createdb.sql
mysql < ./create_song_table.sql
mysql < ./create_writer_table.sql
mysql < ./load_song_data.sql
mysql < ./load_writer_data.sql
mysql < ./createindexes.sql
mysql < ./createuser.sql