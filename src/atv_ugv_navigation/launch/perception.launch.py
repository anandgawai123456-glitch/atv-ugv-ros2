import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('atv_ugv_navigation')
    config = os.path.join(
        pkg,
        'config',
        'perception',
        'scan_filter.yaml'
    )

    scan_filter = Node(
        package='laser_filters',
        executable='scan_to_scan_filter_chain',
        name='scan_filter',
        output='screen',
        parameters=[
            config,
            {'use_sim_time': True},
        ],
        remappings=[
            ('scan', '/scan_raw'),
            ('scan_filtered', '/scan_filtered_raw'),
        ],
    )

    scan_frame_relay = Node(
        package='atv_ugv_navigation',
        executable='scan_frame_relay',
        name='scan_frame_relay',
        output='screen',
        parameters=[
            {'use_sim_time': True},
        ],
    )

    return LaunchDescription([
        scan_filter,
        scan_frame_relay,
    ])
