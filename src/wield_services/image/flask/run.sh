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
    echo "Starting the Flask server"
    echo

    $FLASK_INIT_PATH

fi







