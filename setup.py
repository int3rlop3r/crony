from setuptools import setup, find_packages

setup(
    name='crony',
    version='0.1',
    author='Jonathan Fernandes',
    author_email='int3rlop3r@yahoo.in',
    description='Manage remote crontabs from your terminal',
    url='https://github.com/int3rlop3r/crony',
    packages=find_packages(),
    install_requires=[
        'click',
        'prettytable',
    ],
    entry_points='''
        [console_scripts]
        crony=crony.crony:main
    ''',
)
