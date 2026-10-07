from setuptools import find_packages, setup

package_name = 'atv_ugv_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        (
            'share/' + package_name,
            ['package.xml']
        ),

        (
            'share/' + package_name + '/launch',
            [
                'launch/localization.launch.py',
                'launch/mapping.launch.py',
                'launch/nav2.launch.py',
                'launch/navigation_bringup.launch.py',
                'launch/sim_bringup.launch.py',
                'launch/perception.launch.py',
                'launch/sensors.launch.py',
                'launch/slam.launch.py',
            ]
        ),

        (
            'share/' + package_name + '/config',
            [
                'config/localization.yaml',
                'config/nav2_params.yaml',
                'config/velocity_smoother.yaml',
                'config/collision_monitor.yaml',
                'config/navigation.rviz',
            ]
        ),

        (
            'share/' + package_name + '/config/perception',
            [
                'config/perception/scan_filter.yaml',
            ]
        ),
    ],

    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='anand',
    maintainer_email='anandgawai123456@gmail.com',

    description='TODO: Package description',
    license='TODO: License declaration',

    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
        'console_scripts': [
            'dashboard = atv_ugv_navigation.dashboard:main',
            'scan_frame_relay = atv_ugv_navigation.scan_frame_relay:main',
            'map_rviz_relay = atv_ugv_navigation.map_rviz_relay:main',
            'cmd_vel_stamper = atv_ugv_navigation.cmd_vel_stamper:main',
            'keyboard_teleop = atv_ugv_navigation.keyboard_teleop:main',
            'twist_to_stamped = atv_ugv_navigation.twist_to_stamped:main',
        ],
    },
)
