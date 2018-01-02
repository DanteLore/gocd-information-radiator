#!/bin/bash

ROOT=`pwd`
TARGET=/tmp/gocd-lambda-target
ZIP=~/gocd_lambda.zip
SOURCE_FILES=(go_wrapper gocd_lambda.py)
LIBRARIES=(requests datetime logging json)

# Remove the old zip file
rm -f ${ZIP}

# Create the temp target dir
mkdir ${TARGET}
cd ${TARGET}

# Copy the source files over
for F in ${SOURCE_FILES[@]}; do
    cp -Rf ${ROOT}/${F} ${TARGET}
done

# Install the libraries
for L in ${LIBRARIES[@]}; do
    pip install ${L} -t ${TARGET}
done

# Create the zip file
zip -r ${ZIP} *

# Clean up
rm -rf ${TARGET}

