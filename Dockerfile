# syntax=docker/dockerfile:1

FROM ros:galactic
WORKDIR /mediscara

RUN apt-get update
RUN apt-get install -y wget python3 python3-pip
RUN pip3 install colcon-common-extensions

# clone Integration Service repos
RUN git clone https://github.com/eProsima/Integration-Service.git src/Integration-Service --recursive
RUN git clone https://github.com/eProsima/FIWARE-SH src/FIWARE-SH
RUN git clone https://github.com/eProsima/ROS2-SH src/ROS2_SH

# Integration Service dependencies
RUN apt-get install -y libyaml-cpp-dev libboost-program-options-dev

# FIWARE dependencies
RUN apt-get install -y libcurlpp-dev libasio-dev libcurl4-openssl-dev
ENV IS_ROS2_DISTRO=galactic

COPY is_ws/src/interfaces src/interfaces
COPY is_ws/ros_server.yaml .

COPY docker/launch.sh .
COPY docker/build.sh .

# install packages
RUN bash build.sh

CMD bash # launch.sh