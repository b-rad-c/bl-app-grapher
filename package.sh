#!/bin/bash
NAME="bl_app_grapher"
OUTPUT_PATH="dist/$NAME"

# Remove all __pycache__ folder in project directory.
DIRS_REMOVE=$(find $NAME -name __pycache__ -type d)
if [ -n "${DIRS_REMOVE}" ]
then
    echo "Remove __pycache__ folders"
    echo $DIRS_REMOVE
    find $NAME -name __pycache__ -type d -print0 | xargs -0 rm -r --
    echo
fi

# Create dist folder.
if ! [[ -d "dist" ]]
then
    mkdir -p "dist"
fi

# Zip it all up.
zip -r $OUTPUT_PATH.zip $NAME

echo
echo "Zipped $NAME to $OUTPUT_PATH"
