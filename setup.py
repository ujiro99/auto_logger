from setuptools import setup, find_packages

setup(
    name='autologger',
    version='0.2.0',
    author='Yujiro Takeda',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'pexpect'],
    entry_points={
        "console_scripts": [
            "plog=logger.cli:main",
        ],
    }
)
