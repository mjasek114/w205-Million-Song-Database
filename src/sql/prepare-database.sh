mkdir /tmp/songs
aws s3 sync s3://w205-mmm/merged /tmp/songs

cat /tmp/songs/* > /tmp/Song.csv

mysql < ./createdb.sql
mysql < ./createtable.sql

mysqlimport Songs /tmp/Song.csv
