from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    scan_processor = Node(
        package='atv_ugv_navigation',
        executable='scan_frame_relay',
        name='scan_processor',
        output='screen',
        parameters=[
            {'use_sim_time': True}
        ],
    )

    return LaunchDescription([
        scan_processor,
    ])
