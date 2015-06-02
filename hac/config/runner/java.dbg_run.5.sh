TMPC=$(mktemp -t tmp.XXXX)
printf "handle SIGPWR nostop noprint\nhandle SIGXCPU nostop noprint\nbreak ${TASK}.main\nrun < $FILE_IN" > "$TMPC"
gdb -x "$TMPC" "$TASK"
rm "$TMPC"
