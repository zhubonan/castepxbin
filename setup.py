from setuptools import setup, find_packages
from os import path
import os

version = '0.0.1'
if __name__ == '__main__':

    README_PATH = path.join(path.dirname(__file__), "README.md")

    with open(README_PATH) as f:
        long_desc = f.read()
    setup(
        include_package_data=True,
        packages=find_packages(),
        long_description=long_desc,
        long_description_content_type='text/markdown',
        name='castepxbin',
        author='Bonan Zhu',
        author_email='bon.zhu@protonmail.com',
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Development Status :: 4 - Beta"
        ],
        description="A collection of readers for CASTEP binary outputs",
        url="https://github.com/zhubonan/castepxbin",
        license="MIT License",
        version=version,
        extras_require={'testing': ['pytest', 'sumo']},
        install_requires=["numpy", "six"]
        )