#!/bin/bash
DBNAME=$1

for table in 'globals' 'session' 'questionnaire' 'subjects' 'summary'
do
    ls *_$table.csv > $table
    merge_csvs $table -s $table.csv
    cat $table.csv | psql $DBNAME -c "COPY $table 
                                      FROM STDIN 
                                      WITH (FORMAT csv, HEADER);"
done
