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

    localization_params = os.path.join(
        pkg,
        'config',
        'localization.yaml',
    )

    map_file = os.path.expanduser(
        '~/atv_ugv_jazzy/maps/atv_map.yaml'
    )

    perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(perception_launch)
    )

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'yaml_filename': map_file,
            }
        ],
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            localization_params,
            {
                'use_sim_time': True,

                'global_frame_id': 'map',
                'odom_frame_id': 'odom',
                'base_frame_id': 'base_footprint',

                'scan_topic': '/scan_filtered',
                'map_topic': '/map',

                'tf_broadcast': True,

                'set_initial_pose': True,
                'initial_pose.x': 0.0,
                'initial_pose.y': 0.0,
                'initial_pose.z': 0.0,
                'initial_pose.yaw': 0.0,
            },
        ],
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                    'map_server',
                    'amcl',
                ],
                'bond_timeout': 4.0,
            }
        ],
    )

    return LaunchDescription([
        perception,
        map_server,
        amcl,
        lifecycle_manager,
    ])
