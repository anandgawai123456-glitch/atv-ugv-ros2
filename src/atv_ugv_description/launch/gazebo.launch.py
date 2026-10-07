import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    pkg_name = 'atv_ugv_description'
    pkg_share = get_package_share_directory(pkg_name)
    install_dir = os.path.dirname(pkg_share)

    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'ugv.urdf.xacro'
    )

    world_file = os.path.join(
        pkg_share,
        'worlds',
        'atv_navigation_world.sdf'
    )

    robot_desc = xacro.process_file(xacro_file).toxml()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_desc,
                'use_sim_time': True
            }
        ]
    )

    set_gz_path = SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
             value=install_dir
                            
    )

    set_ign_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=[
            install_dir,
            ':',
            os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
        ]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-string',
            robot_desc,
            '-name',
            'atv_ugv',
            '-z',
            '0.15'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/world/atv_navigation_world/model/atv_ugv/link/base_footprint/'
            'sensor/lidar/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'
        ],
        remappings=[
            (
                '/world/atv_navigation_world/model/atv_ugv/link/base_footprint/'
                'sensor/lidar/scan',
                '/scan_raw'
            )
        ],
        output='screen'
    )
    
    cmd_vel_stamper = Node(
        package='atv_ugv_navigation',
        executable='cmd_vel_stamper',
        remappings=[
            ('/cmd_vel_stamped', '/diff_drive_controller/cmd_vel')
        ],
        output='screen'
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60'
        ],
        output='screen'
    )

    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60'
        ],
        output='screen'
    )

    start_diff_drive = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster,
            on_exit=[diff_drive_controller]
        )
    )

    return LaunchDescription([
        set_gz_path,
        set_ign_path,
        robot_state_publisher,
        gazebo,
        spawn_entity,
        bridge,
        joint_state_broadcaster,
        start_diff_drive,
        cmd_vel_stamper
    ])
