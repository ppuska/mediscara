from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package='mediscara',
                executable="marker_node"
            ),
            Node(
                package='mediscara',
                executable="robot2_node"
            )
        ]
    )
