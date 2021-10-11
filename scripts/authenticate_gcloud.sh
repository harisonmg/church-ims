#! /bin/bash

# create GOOGLE_APPLICATION_CREDENTIALS if it doesn't exist
if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "$GOOGLE_CREDENTIALS" > "$GOOGLE_APPLICATION_CREDENTIALS"
fi

# authenticate gcloud
gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
