echo "Building the Integration service package"

msg_packages=()

for package in $(ls is_ws/src)
do
    if test -d is_ws/src/${package}/msg; then
        echo "ROS messages found in" $package
        if test ${#msg_packages[@]} -eq 0; then # first element in array
            msg_packages+="$package"
        else
            msg_packages+=" $package"
        fi
    fi
done

cmd="colcon build --allow-overriding $(ls is_ws/src) "
cmd+="--cmake-args -DMIX_ROS2_PACKAGES=\"${msg_packages}\" "

eval $cmd || error=1

if test $error; then
    echo "Rebuilding..."
    source is_ws/install/setup.bash

    eval $cmd "--packages-select-build-failed" || return 1

return 0