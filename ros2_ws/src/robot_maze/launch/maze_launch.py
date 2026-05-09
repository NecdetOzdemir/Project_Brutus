import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Paket yolları
    pkg_robot_maze = get_package_share_directory('robot_maze')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # World ve SDF yolları
    world_file = os.path.join(pkg_robot_maze, 'worlds', 'maze.world')
    robot_sdf = os.path.join(pkg_robot_maze, 'models', 'maze_robot', 'model.sdf')

    # 1. Gazebo Fortress'ı Başlat (Ignition)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -v 4 {world_file}' # -r: otomatik başlat, -v 4: detaylı log
        }.items()
    )

    # 2. Robotu Simülasyona Ekle (Spawn)
    spawn_robot = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-name', 'brutus_robot',
                    '-file', robot_sdf,
                    '-x', '-2.5',   # Sol alt köşe
                    '-y', '-2.5',
                    '-z', '0.1',
                    '-Y', '1.5708', # 90° yönlenme (kuzey)
                ],
                output='screen',
            )
        ]
    )

    # 3. ROS 2 <-> Gazebo Köprüsü (Sensör ve Motor Haberleşmesi)
    # Fortress'ta veriler otomatik akmaz, bu köprü sayesinde ROS'a geçer
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
        bridge
    ])
