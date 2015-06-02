# Preprocess: replace "class temp"
warn "Preprocessing language templated... if needed!"
sed -i "s/class [^{\ ]\+/class ${TASK}/" "${TASK}.${EXT_SRC}"

javac -g -cp ".;*" "${TASK}.${EXT_SRC}"
gcj -g --main="${TASK}" -o "${TASK}" "${FILE_EXEC}"
