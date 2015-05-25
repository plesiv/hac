sed -i "s/class [^{\ ]\+/class ${TASK}/" "${TASK}.${EXT_SRC}"
javac -g:none -cp ".;*" "${TASK}.${EXT_SRC}"
