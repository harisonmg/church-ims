#! /bin/bash

DJANGO_SETTINGS_MODULE=config.settings.production
export STATIC_FILES_DIR=gs://"$GCP_STORAGE_BUCKET_NAME"/static

# Collect the static files
echo "Collecting static files"
python manage.py collectstatic --no-input

# Synchronize the content of the source bucket with other buckets
IFS=',' read -r -a storage_buckets <<< "$DESTINATION_STORAGE_BUCKET_NAMES"

for bucket_name in "${storage_buckets[@]}"; do
    export bucket="$STATIC_FILES_DIR"
    export bucket="${bucket/$GCP_STORAGE_BUCKET_NAME/$bucket_name}"
    gsutil -m rsync -d -r "$STATIC_FILES_DIR" "$bucket"
done
