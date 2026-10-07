import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    description_pkg = get_package_share_directory(
        'atv_ugv_description'
    )

    navigation_pkg = get_package_share_directory(
        'atv_ugv_navigation'
    )

    gazebo_launch = os.path.join(
        description_pkg,
        'launch',
        'gazebo.launch.py'
    )

    navigation_launch = os.path.join(
        navigation_pkg,
        'launch',
        'navigation_bringup.launch.py'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch)
    )

    navigation = TimerAction(
        period=8.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(navigation_launch)
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        navigation
    ])
