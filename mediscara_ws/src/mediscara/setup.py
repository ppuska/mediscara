import os
from glob import glob

from setuptools import find_packages, setup

package_name = "mediscara"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # Include all launch files. This is the most important line here!
        (os.path.join("share", package_name), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools", "mysql-connector-python"],
    zip_safe=True,
    maintainer="Peter Puska",
    maintainer_email="p.puska@lasram.hu",
    description="",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "marker_node = mediscara.marker_node:main",
            "robot1_node = mediscara.robot1_node:main",
            "robot2_node = mediscara.robot2_node:main",
            "collab_node = mediscara.hmi_collab_node:main",
            "robotic_node = mediscara.hmi_robotic_node:main",
        ],
    },
)
