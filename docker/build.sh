#! /bin/bash

source /opt/ros/galactic/setup.bash

colcon build --packages-skip is-ros2-mix-generator

source install/setup.bash

colcon build --packages-skip-build-finished --cmake-args -DMIX_ROS2_PACKAGES="interfaces"

source install/setup.bash