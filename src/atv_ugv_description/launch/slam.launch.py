from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    slam = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[
            '/home/anand/atv_ugv_jazzy/src/atv_ugv_description/config/slam_mapper.yaml'
        ],
        output='screen'
    )

    return LaunchDescription([
        slam
    ])
