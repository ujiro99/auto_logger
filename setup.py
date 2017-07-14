from setuptools import setup, find_packages

setup(
    name='autologger',
    version='0.1.0',
    author='Yujiro Takeda',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'pexpect'],
)
