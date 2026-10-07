import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('atv_ugv_navigation')

    perception_launch = os.path.join(
        pkg,
        'launch',
        'perception.launch.py',
    )

    slam_params = os.path.join(
        pkg,
        'config',
        'localization.yaml',
    )

    perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(perception_launch)
    )

    slam = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params,
            {
                'use_sim_time': True,
                'scan_topic': '/scan_filtered',
            },
        ],
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_slam',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'scan_topic': '/scan_filtered',
                'autostart': True,
                'node_names': ['slam_toolbox'],
            }
        ],
    )

    return LaunchDescription([
        perception,
        slam,
        lifecycle_manager,
    ])
