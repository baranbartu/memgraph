
from setuptools import setup

setup(
    name='memgraph',
    version='0.0.1',
    packages=['memgraph'],
    url='http://github.com/baranbartu/memgraph',
    license='MIT',
    author='Baran Bartu Demirci',
    author_email='bbartu.demirci@gmail.com',
    description='memory observation and graph tool for methods',
    install_requires=['guppy','plotly']
)
