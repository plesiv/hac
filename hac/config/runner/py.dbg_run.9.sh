TMPC=$(mktemp tmp.XXXX)
sed "1 i\
#vvv MONKEY-PATCHED\
\ndef input(f=open(\"${FILE_IN}\")): return f.readline().rstrip()\
\ndef raw_input(f=open(\"${FILE_IN}\")): return f.readline().rstrip()\
\n#^^^ MONKEY-PATCHED\n" \
"$FILE_EXEC" > "$TMPC"
pudb "$TMPC"
rm "$TMPC"
