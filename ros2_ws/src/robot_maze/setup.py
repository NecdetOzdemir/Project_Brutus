import os
from glob import glob
from setuptools import setup

package_name = 'robot_maze'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch dosyalarını kopyala
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # World dosyalarını kopyala
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        # Robot model dosyalarını kopyala
        (os.path.join('share', package_name, 'models/maze_robot'), glob('models/maze_robot/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='necdet',
    maintainer_email='necdet@todo.todo',
    description='Project Brutus - PPO tabanlı labirent navigasyon paketi',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Gelecekte buraya train ve env scriptlerini ekleyeceğiz
        ],
    },
)
