from setuptools import setup

setup(
    name='crony',
    version='0.1',
    py_modules=['crony'],
    install_requires=[
        'click',
        'prettytable',
    ],
    entry_points='''
        [console_scripts]
        crony=crony.crony:crony
    ''',
)
