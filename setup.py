from setuptools import find_packages, setup

NAME = "betterenvs"
VERSION = "1.0.0"
REQUIREMENTS = ["PyYAML==6.0.1"]

setup(
    name=NAME,
    version=VERSION,
    description='A production-ready library for handling environment variables and settings',
    url='https://github.com/PhantomWall/phantom-tools.git',
    author="Alex Christian",
    author_email='13alexchristian@example.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=REQUIREMENTS,
    setup_requires=["pytest-runner"],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
)
