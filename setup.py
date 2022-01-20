# Added for legacy
from setuptools import setup

packages = ["slurmer"]

package_data = {"": ["*"], "slurmer": ["templates/*"]}

install_requires = ["Jinja2>=3.0.3,<4.0.0", "tinydb>=4.6.1,<5.0.0"]

setup_kwargs = {
    "name": "slurmer",
    "version": "0.2.0",
    "description": "",
    "author": "Minjoon Hong",
    "author_email": "mjhong0708@yonsei.ac.kr",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
