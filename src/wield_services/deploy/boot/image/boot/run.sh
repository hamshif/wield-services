#!/bin/bash

$PACKAGE_PY_PATH

if [[ "$CONTAINER_MAINTAINANCE_MODE" == 'yup' ]] ; then
    echo "Starting dud process to enable development debugging"

    while :
    do
        sleep 100
    done
else

    printenv
    echo
    echo "Running Perl script"
    echo

    perl /app/pep.pl

fi







