# Preprocess: replace "class temp"
warn "Preprocessing language templated... if needed!"
sed -i "s/class [^{\ ]\+/class ${TASK}/" "$FILE_SRC"

javac -g:none -cp ".;*" "${TASK}.${EXT_SRC}"
