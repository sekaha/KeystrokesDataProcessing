for FOLDER in $(find ./files/ -mindepth 1 -maxdepth 1 -type d); do
    rm -r "$FOLDER"
    echo "removed folder $FOLDER"
done