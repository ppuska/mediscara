#! /bin/bash

echo "This is an installation script for the MediScara project"

usage() {
    echo "Usage $0 [ -o Allow Overriding packages]" 1>&2
}

error_result() {
    echo "Error installing ROS packages"
}

mediscara_install() {
    if test $allow_overriding; then
        echo "Overriding packages"
        colcon build --allow-overriding $(ls src) || return 1
    else
        colcon build || return 1
        echo
    fi
}

is_install() {
    echo "Installing ROS Nodes to Integration Service"

    cmd="colcon build "
    if test $allow_overriding; then
        cmd+="--allow-overriding $(ls src) "
    fi

    if test ${#msg_packages[@]} -ne 0; then
        cmd+="--cmake-args -DMIX_ROS2_PACKAGES=\"${msg_packages}\" "
    fi

    eval $cmd || error=1

    if test $error; then
        echo "Packages failed, sourcing local setup.bash then trying again"
        source install/setup.bash

        eval ${cmd} "--packages-select-build-failed"
    fi
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

cd mediscara_ws

mediscara_install  || error_result

echo "Installing Integration Service"

cd ..   # back to launch.sh pwd

echo "Overriding packages with msg directories..."

msg_packages=()

for package in $(ls mediscara_ws/src)
do
    if test -d mediscara_ws/src/${package}/msg; then
        echo "ROS messages found in" $package
        if test ${#msg_packages[@]} -eq 0; then # first element in array
            msg_packages+="$package"
        else
            msg_packages+=" $package"

        cp -r mediscara_ws/src/$package is_ws/src
        fi
    fi
done

cd is_ws

is_install || error_result

cd ..

echo "Packages successfully installed"


