#! /bin/bash

echo "This is an installation script for the MediScara project"

usage() {
    echo "Usage $0 [ -o Allow Overriding packages]" 1>&2
}

# get command line options
while getopts o flag
do
    case ${flag} in
        o) allow_overriding=1;;
        *) usage ; exit 1; ;;
    esac
done

echo "Installing ROS nodes"
if test allow_overriding; then
    colcon build --allow_overriding $(ls src) || error=1
else
    colcon build || error=1
fi

if test $error; then
    echo "Error installing ROS packages"
    exit 1;
fi

echo "Installing Integration Service"
