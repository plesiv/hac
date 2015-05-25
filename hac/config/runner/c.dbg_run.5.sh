TMPC=$(mktemp -t tmp.XXXX)
printf "break main\nrun < $FILE_IN" > "$TMPC"
gdb -x "$TMPC" "$FILE_EXEC"
rm "$TMPC"
