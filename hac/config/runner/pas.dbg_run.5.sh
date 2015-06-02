TMPC=$(mktemp -t tmp.XXXX)
printf "break main\nrun < $FILE_IN" > "$TMPC"
gdb -q -x "$TMPC" "$FILE_EXEC"
rm "$TMPC"
