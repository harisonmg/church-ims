#!/bin/bash

export BASE_DIR=.
export DB_DOCS_DIR="$BASE_DIR"/docs/db
migrations_sql_file="$DB_DOCS_DIR"/migrations.sql
showmigrations_output="$DB_DOCS_DIR"/migrations.txt

rm -rf "$DB_DOCS_DIR"
mkdir "$DB_DOCS_DIR"
touch "$migrations_sql_file"

# get the migrations for all apps
python manage.py showmigrations > "$showmigrations_output"
while IFS=$'\r\n' read -r line; do
    array=( $line ) 
    last_element=${array[-1]}

    # get the app labels and migration names
    if [[ (! "$last_element" =~ "migrations") && (! "$last_element" =~ ^[0-9]+) ]]; then
        app_label="$last_element"
    fi

    # the previous app label is not set or previous app label
    # is equal to the current app label
    condition="( test -z $previous_app_label) || [ $app_label == $previous_app_label ]"
    if $(eval "$condition"); then
        if [[ "$last_element" =~ ^[0-9]+ ]]; then
            migration_name="$last_element"
            echo "$app_label: $migration_name"
            echo "---------------------------"
            echo ""
            python manage.py sqlmigrate "$app_label" "$migration_name" >> "$migrations_sql_file"
        fi
    fi
    previous_app_label="$app_label"
done < "$showmigrations_output"
