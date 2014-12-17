# This file is intended to help the developer
# to create the database for storing RED-I stats
# about completed runs as well as to insert/select
# sample data for testing.


DB_FILE        := redi_runs.db
SCHEMA_SQLITE  := dump_sqlite.sql
SCHEMA_MYSQL   := dump_mysql.sql

# File name - stores queries for creating tables
SQL_UPGRADE          := sql/upgrade.sql

# File name - stores queries for dropping all tables/data
SQL_DOWNGRADE        := sql/downgrade.sql

# File name - stores queries for inserting sample data
SQL_INSERT_FILE      := sql/insert.sql

# File name - stores examples for reading data
SQL_SELECT_ALL_FILE  := sql/sample_queries.sql

# Queries for most common tasks
SQL_SAMPLE_SELECT_RUNS := 'SELECT * FROM Project NATURAL JOIN Site NATURAL JOIN SiteRun WHERE prjID = 1 ORDER BY siteName, srDate'
SQL_SAMPLE_SELECT_RUND := 'SELECT * FROM Project NATURAL JOIN Site NATURAL JOIN SiteRun NATURAL JOIN SiteRunData WHERE prjID = 1 ORDER BY siteName, srDate'
SQL_SAMPLE_SELECT    := '\
SELECT \
   prjName, siteName, srDate, frmName, srdSubjectID, srdFormCount \
FROM \
   Project \
   JOIN Site USING (prjID) \
   JOIN SiteRun USING (siteID) \
   JOIN SiteRunData USING (srID) \
   JOIN Form USING (frmID) \
WHERE \
   1 '

help:
	@echo "Available tasks:"
	@echo "\t show_tables            : show the tables in the database"
	@echo "\t show_schema            : show the database DDL statements"
	@echo "\t upgrade                : create fresh tables by executing queries from '$(SQL_UPGRADE)' "
	@echo "\t downgrade              : drop created tables by executing queries from '$(SQL_DOWNGRADE)' "
	@echo "\t sample_data_insert     : insert sample data"
	@echo "\t sample_data_select     : select sample data"
	@echo "\t sample_data_select_all : select all sample data"
	@echo "\t sample_data_select_runs: select all data from 'SiteRun' table"
	@echo "\t sample_data_select_rund: select all data from 'SiteRunData' table"
	@echo "\t dump                   : save sqlite schema to the file '$(SCHEMA_SQLITE)' "
	@echo "\t convert                : convert sqlite tables from '$(DB_FILE)' to the file $(SCHEMA_MYSQL)"

run_app:
	python app/rediapi.py &

show_tables:
	sqlite3 $(DB_FILE) .tables

show_schema:
	sqlite3 $(DB_FILE) .dump > $(SCHEMA_SQLITE)
	cat $(SCHEMA_SQLITE)

upgrade:
	sqlite3 $(DB_FILE) '.read $(SQL_UPGRADE)'

downgrade:
	sqlite3 $(DB_FILE) '.read $(SQL_DOWNGRADE)'

sample_data_insert:
	sqlite3 $(DB_FILE) '.read $(SQL_INSERT_FILE)'

sample_data_select:
	sqlite3 $(DB_FILE) $(SQL_SAMPLE_SELECT)

from_scratch:
	make downgrade && make upgrade && make sample_data_insert && make sample_data_select_all

sample_data_select_all:
	sqlite3 $(DB_FILE) '.read $(SQL_SELECT_ALL_FILE)'

sample_data_select_runs:
	sqlite3 $(DB_FILE) $(SQL_SAMPLE_SELECT_RUNS)

sample_data_select_rund:
	sqlite3 $(DB_FILE) $(SQL_SAMPLE_SELECT_RUND)

convert:
	sqlite3 $(DB_FILE) .dump | python scripts/sqlite_to_mysql.py > $(SCHEMA_MYSQL)
	@cat $(SCHEMA_MYSQL)

clean:
	rm -f *.pyc
	rm -f $(SCHEMA_SQLITE)
	rm -f $(SCHEMA_MYSQL)
