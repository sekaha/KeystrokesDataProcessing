for FILE in $(find ./files/ -maxdepth 1 -type f -name "*.txt" -printf "%f\n"); do
    rm "./files/$FILE"
    echo "removed file $FILE"
done