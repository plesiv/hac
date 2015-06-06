#!/bin/sh
# Copyright (C) 2014-2015  Zoran Plesivčak <z@plesiv.com>
# This software is distributed under the terms of the GNU GPL version 2.

# Posix shell compatible runner script.

#TODO: Measure exec time.
#TODO: Measure exec memory.

# -- Variables ----------------------------------------------------------------
FILE_RUNNER=${0##./}     # Remove possible './'
TASK=${FILE_RUNNER%%.*}  # Remove all the extensions
EXT_IN=in
EXT_OUT=out
EXT_MYOUT=my.out
for LARG; do true; done; # Last CLI argument

#vvv templated
$variables
#^^^ templated

# OS dependent message coloring
if [[ "$OSTYPE" == "darwin"* ]]; then
    C_OK="\033[1;32m"
    C_ERROR="\033[1;34m"
    C_END="\033[0m"
else
    C_OK="\e[1;32m"
    C_ERROR="\e[1;34m"
    C_END="\e[0m"
fi


# -- Utility functions --------------------------------------------------------
#
# Functions for handling errors.
#
warn() {
    echo -e "$*" >&2
}
die () {
    echo -e "$*" >&2
    exit 1
}

#
# Pipe function for whitespace-normalization of text.
#
normalize_pipe() {
    # append newline     | squeeze spaces  | squeeze newlines
    (cat -; printf "\n") | tr -s " "       | tr -s "\n"
}

#
# Compares files and prints message about how they relate.
#
compare_files() {
    TC="${3:-UNKOWN}"

    # Input verification
    if [ -z "$1" ] || [ -z "$2" ]; then
        error "Testcase ${TC}: ${C_ERROR}ERROR: Filename empty!${C_END}"
        return 1
    fi

    if [ ! -f "$1" ] || [ ! -f "$2" ]; then
        error "Testcase ${TC}: ${C_ERROR}ERROR: File doesn't exist!${C_END}"
        return 1
    fi

    # Prepare files for comparison
    TMP1=$(mktemp -t tmp.XXXX)
    TMP2=$(mktemp -t tmp.XXXX)
    cat "$1" | normalize_pipe >"$TMP1"
    cat "$2" | normalize_pipe >"$TMP2"

    # Compare temp files and save output
    DIFF_TMP=$(diff -u --label="Answer" --label="Output" "$TMP1" "$TMP2")

    if [ $? -eq 0 ]; then
        echo -e "Testcase ${TC}: ${C_OK}OK${C_END}"
    else
        echo -e "Testcase ${TC}: ${C_ERROR}Wrong Answer${C_END}"
        echo "$DIFF_TMP"
    fi

    # Clean temp files
    rm "$TMP1" "$TMP2"
}


# -- Process command line arguments -------------------------------------------
COMMAND=

if [ "$#" -ne 0 ]; then
    while getopts ":ced" opt; do
        case $opt in
            c)  [ -n "$COMMAND" ] &&
                die "${C_ERROR}ERROR: Options are mutually exclusive!${C_END}"
                COMMAND=c ;;
            e)  [ -n "$COMMAND" ] &&
                die "${C_ERROR}ERROR: Options are mutually exclusive!${C_END}"
                COMMAND=e ;;
            d)  [ -n "$COMMAND" ] &&
                die "${C_ERROR}ERROR: Options are mutually exclusive!${C_END}"
                COMMAND=d ;;
            \?) die "${C_ERROR}ERROR: Invalid option: -$OPTARG${C_END}"
        esac
    done
fi


# -- Run command --------------------------------------------------------------
# 1) Show usage instructions
if [ -z "$COMMAND" ]; then
cat <<EOF
usage: ./${FILE_RUNNER} [-c | -e | -d TESTCASE]

optional arguments:
  -c            clean files created by previous runs (executables,
                outputs etc.)
  -e            run all test-cases and compare them with expected answers
  -d TESTCASE   debug program for specified test-case


EXAMPLE ... to debug program for second test-case execute:

    ./${FILE_RUNNER} -d 2

EOF
fi

# 2) Clean executable and outputs
if [ "$COMMAND" == c ]; then
    echo "Cleaning..."
    #vvv templated
    $clean
    #^^^ templated
fi

# 3) Compile source, run executable, compare output
if [ "$COMMAND" == e ]; then

    # Compile source
    #vvv templated
    $exec_compile
    #^^^ templated

    for FILE_IN in ${TASK}.*.${EXT_IN}
    do
        TC=${FILE_IN%%.$EXT_IN}
        FILE_OUT="${TC}.${EXT_OUT}"
        FILE_MYOUT="${TC}.${EXT_MYOUT}"

        # Run program
        #vvv templated
        $exec_run
        #^^^ templated

        # Compare results
        compare_files "$FILE_OUT" "$FILE_MYOUT" "$TC"
    done
fi

# 4) Compile source, debug executable
if [ "$COMMAND" == d ]; then

    # Compile source
    #vvv templated
    $dbg_compile
    #^^^ templated

    TC=${FILE_IN%%.$EXT_IN}
    FILE_IN="${TASK}.${LARG}.${EXT_IN}"

    if [ ! -f "$FILE_IN" ]; then
        die "${C_ERROR}ERROR: File \"${FILE_IN}\" doesn't exist!${C_END}"
    fi

    # Debug executable
    #vvv templated
    $dbg_run
    #^^^ templated
fi
