#!/bin/sh
# Copyright (C) 2014-2015  Zoran Plesivčak <z@plesiv.com>
# This software is distributed under the terms of the GNU GPL version 2.

# Posix shell compatible runner script. 

#TODO: Add optimization flags
#TODO: CLI switch for "clean" command
#TODO: Measure exec time
#TODO: Measure exec memory
#TODO: Debugging (start debugger on given test-case)
#TODO: CLI switch for other compiler

# -- Common variables ---------------------------------------------------------
FNAME_RUNNER=${0##./}           # Remove possible './'
TASK=${FNAME_RUNNER%%.*}        # Remove all the extensions
EXT_INPUT=in
EXT_OUTPUT=out

# -- Language specific variables ----------------------------------------------
$variables


# -- Utilities ----------------------------------------------------------------
normalize_stdin() {
    # append newline     | compress spaces | compress newlines
    (cat -; printf "\n") | tr -s " "       | tr -s "\n"
}

compare_files() {
    TESTCASE="$3"

    # Prepare files for comparison
    TMP1=$(mktemp -t tmp.XXXX)
    TMP2=$(mktemp -t tmp.XXXX)
    cat "$1" | normalize_stdin >"$TMP1"
    cat "$2" | normalize_stdin >"$TMP2"

    # Compare temp files and save output
    DIFF_TMP=$(diff -u --label="Answer" --label="Output" "$TMP1" "$TMP2")

    if [ $? -eq 0 ]; then
        echo -e "Testcase ${TESTCASE}: \e[1;32mOK\e[0m"
    else
        echo -e "Testcase ${TESTCASE}: \e[1;31mWrong Answer\e[0m"
        echo "$DIFF_TMP"
    fi

    # Clean temp files
    rm "$TMP1" "$TMP2"
}


# -- Compile ------------------------------------------------------------------
$compile


# -- Execute ------------------------------------------------------------------
for FNAME_INPUT in *.$EXT_INPUT
do
    TESTCASE=${FNAME_INPUT%%.$EXT_INPUT}
    FNAME_OUTPUT="${TESTCASE}.${EXT_OUTPUT}"
    FNAME_MYOUTPUT="${TESTCASE}.my.${EXT_OUTPUT}"

    # Execute and save results
    $execute

    # Compare results
    compare_files "$FNAME_OUTPUT" "$FNAME_MYOUTPUT" "$TESTCASE"
done


