# Rename the files to just their number
# $(find . -type f -name "*_keystrokes.txt" -printf "%f\n")
for FILE in *; do
	NEW_NAME=$(echo "$FILE" | sed 's/_.*//') # keep only number
	NEW_NAME=$(printf "%06d" "$NEW_NAME") # format it to have leading zeros
	NEW_NAME="${NEW_NAME}.txt" # save it as a textfile
	mv "$FILE" "$NEW_NAME" # rename, jank kinda?
	echo "moved $FILE to $NEW_NAME"
done