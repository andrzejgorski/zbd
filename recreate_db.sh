#!bin/bash
cat drop_tables.sql | sqlite3 baza_dblp.sqlite3; cat create_database_schema.sql | sqlite3 baza_dblp.sqlite3
