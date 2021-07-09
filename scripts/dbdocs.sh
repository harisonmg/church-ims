#!/bin/bash

export BASE_DIR=.
export DB_DOCS_DIR="$BASE_DIR"/docs/db/
migrations_sql_file="$DB_DOCS_DIR"/migrations.sql
migrations_dbml_file="$DB_DOCS_DIR"/migrations.dbml

# install dbdocs and dbml cli
# https://www.dbml.org/cli/
# npm install -g @dbml/cli
# npm install -g dbdocs

# login to dbdocs
# https://dbdocs.io/docs
# dbdocs login 

# clean the migrations SQL file
comment="s/^/--/g"
delete="d"
sed "/BEGIN/${delete};/COMMIT/${delete};" -i "$migrations_sql_file"
sed "/INDEX/${comment};/CONSTRAINT/${comment};/SEQUENCE/${comment};" -i "$migrations_sql_file"
sed "/USING/${comment}" -i "$migrations_sql_file"
sed -e "/DROP COLUMN/${comment};" -i "$migrations_sql_file"


# generate dbml from SQL
sql2dbml "$migrations_sql_file" -o "$migrations_dbml_file"

# generate documentation
dbdocs build "$migrations_dbml_file" --project="church-ims"

# clean up
rm -rf "$DB_DOCS_DIR"
