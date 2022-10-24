# Filename    : setup.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

from setuptools import setup, find_packages
from sys import path
from os import environ

path.insert(0, '.')

NAME = "myresume"

if __name__ == "__main__":

    setup(
        name=NAME,
        version='0.0.1',
        author="Jonathan Kelley",
        author_email="jonk@omg.lol",
        url="https://github.com/jondkelley/python_resume",
        license='ASLv2',
        packages=find_packages(),
        include_package_data=True,
        package_dir={NAME: NAME},
        description="myresume - Interactive online resume for jon-kelley.com",
        install_requires=['Flask==2.1.0', 'python-slugify', 'markdown', 'Jinja2==3.0.3', 'werkzeug==2.0.2'],
        entry_points={
            'console_scripts': ['myresume = myresume.runserver:main'],
        },
        zip_safe=False,
    )
