#!/bin/bash
while getopts f:d: flag
do
    case "${flag}" in
        f) filename="${OPTARG}";;
        d) timestamp="${OPTARG}";;
    esac
done

echo "Filename: ${filename}"
echo "Timestamp: ${timestamp}"

cd temp
echo 'Deleting Archives if they exist'
FOLDER_NAME="${timestamp}_${filename%.zip}"
rm -rf ${FOLDER_NAME}
echo 'Uncompressing Files'
unzip -q "../uploads/${timestamp}_${filename}"
mv ${filename%.zip} $FOLDER_NAME
cd ..

donkey train --tub temp/${FOLDER_NAME} --model models/${timestamp}_${filename%.zip}.h5 --type linear --config config.py

rm -rf temp/${FOLDER_NAME}


