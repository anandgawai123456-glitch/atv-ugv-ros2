import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('atv_ugv_navigation')

    gazebo_launch = os.path.join(
        get_package_share_directory('atv_ugv_description'),
        'launch',
        'gazebo.launch.py',
    )

    localization_launch = os.path.join(
        pkg,
        'launch',
        'localization.launch.py',
    )

    nav2_launch = os.path.join(
        pkg,
        'launch',
        'nav2.launch.py',
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch)
    )

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(localization_launch)
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_launch)
    )

    rviz_config = os.path.join(pkg, 'config', 'navigation.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[
            {
                'use_sim_time': True,
                'qos_overrides./map.subscription.reliability': 'reliable',
                'qos_overrides./map.subscription.durability': 'transient_local',
                'qos_overrides./map.subscription.history': 'keep_last',
                'qos_overrides./map.subscription.depth': 1,
            }
        ],
    )

    return LaunchDescription([
        localization,
        nav2,
        rviz,
    ])
