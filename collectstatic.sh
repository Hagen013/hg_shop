#!/bin/bash

# FRONTEND

cd ./frontend;
# npm i;
npm  run build;
gulp build;

# BACKEND
cd ../..;
source ./venv/bin/activate;
cd ./project/backend/;
python manage.py collectstatic --settings=config.settings.production --noinput;
deactivate;
cd ..

# ADD HASH TO STATIC FILE NAMES IN 
# STATIC FILES AND IN TEMPLATES
hash_suffix="$(date | md5sum | cut -c1-7)"
echo "HASH_SUFFIX=${hash_suffix}"

TEMPLATES_PATH="$(cd ./frontend/templates && pwd && cd ../..)"
echo "TEMPLATES_PATH=${TEMPLATES_PATH}"

# # STATIC FILES
cd ./compose/nginx/staticfiles;
STATIC_FILE_PATHS=(
    "css/styles.css"
    "js/scripts.js"
    "js/categoryPage.js"
    "js/productPage.js"
    "js/cartPage.js"
    "js/orderPage.js"
    "js/infoPage.js"
)

# # REPLACE STATIC FILES AND TEMPLATES
for file_name in ${STATIC_FILE_PATHS[@]}
do
    new_file_name="${file_name%%.*}_${hash_suffix}.${file_name#*.}"
    cp $file_name $new_file_name
    find $TEMPLATES_PATH -name '*.html' -exec sed -i "s/$(sed 's/\//\\\//g' <<< $file_name)/$(sed 's/\//\\\//g' <<< $new_file_name)/g" '{}' \;
    echo "${file_name} hashed"
done
