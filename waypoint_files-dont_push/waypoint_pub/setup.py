from setuptools import find_packages, setup

package_name = 'waypoint_pub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mcav',
    maintainer_email='s.a.baaset.moslih@gmail.com',
    description='A simple package used for publishing a fixed global waypoint with a radius',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          #     node_name = package_name.node file_name:main
            'waypoint_pub = waypoint_pub.waypoint_publisher:main'
        ],
    },
)
