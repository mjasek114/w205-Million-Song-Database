#!/bin/bash

hive -f ascap.sql
hive -f billboard.sql
hive -f key.sql
hive -f million_song_dataset.sql
hive -f analysis.sql