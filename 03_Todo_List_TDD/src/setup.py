from setuptools import setup, find_packages

setup(
    name='todo', 
    packages=find_packages(include=['todo', 'todo.*']),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    
    )