from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'robot_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # (os.path.join('share', package_name, 'launch'),glob(os.path.join('launch', '*.launch.py')) + glob(os.path.join('launch', '*.launch.xml'))),
        *[(os.path.join('share', package_name, os.path.dirname(p)), [p]) for pattern in ('launch/**/*.launch.py', 'launch/**/*.launch.xml') for p in glob(pattern, recursive=True)],

        *[(os.path.join('share', package_name, os.path.dirname(p)), [p]) for p in glob('config/**/*.yaml', recursive=True)],
        # (os.path.join('share', package_name, 'config'),glob('config/*.yaml')),

        *[(os.path.join('share', package_name, os.path.dirname(p)), [p]) for p in glob('rviz/**/*.rviz', recursive=True)],

    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hcic',
    maintainer_email='hcic@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # 'test_nav = robot_nav.test_nav:main',
            'pointcloud_transform_node = robot_nav.pointcloud_transform:main',
        ],
    },
)
