sed -i "s/class [^{\ ]\+/class ${TASK}/" "${TASK}.${EXT_SRC}"
javac -g -cp ".;*" "${TASK}.${EXT_SRC}"
