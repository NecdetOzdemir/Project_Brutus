"""
╔══════════════════════════════════════════════════════════════╗
║  Project Brutus - Gazebo Launch Dosyası                      ║
║                                                              ║
║  Başlatır:                                                   ║
║    1. Gazebo (maze.world ile)                               ║
║    2. Robot spawn (brutus_robot, sol-alt köşeden)           ║
║    3. robot_state_publisher (TF yayınlar)                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Paket yolları
    pkg_robot_maze = get_package_share_directory('robot_maze')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # World dosyası yolu
    world_file = os.path.join(pkg_robot_maze, 'worlds', 'maze.world')

    # Robot model (SDF) yolu
    robot_sdf = os.path.join(pkg_robot_maze, 'models', 'maze_robot', 'model.sdf')

    # ── Gazebo Çökme Önleyici Ayarlar (NVIDIA/Hybrid GPU Fix) ──
    # Bu ayarlar Camera Assertion hatasını engeller
    env_vars = [
        SetEnvironmentVariable('LC_NUMERIC', 'C'),
        SetEnvironmentVariable('MESA_GL_VERSION_OVERRIDE', '4.1'),
        SetEnvironmentVariable('__NV_PRIME_RENDER_OFFLOAD', '1'),
        SetEnvironmentVariable('__GLX_VENDOR_LIBRARY_NAME', 'nvidia'),
        SetEnvironmentVariable('GAZEBO_MODEL_DATABASE_URI', ''), # Online veritabanı beklemesini iptal eder
    ]

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_file,
            'verbose': 'true',
            'pause': 'false',
        }.items()
    )

    # ── Robot Spawn ───────────────────────────────────────────
    # Gazebo'nun hazır olmasını beklemek için 3 saniye gecikme
    spawn_robot = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=[
                    '-entity', 'brutus_robot',
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

    return LaunchDescription(env_vars + [
        gazebo,
        spawn_robot,
    ])
