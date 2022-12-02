from setuptools import find_packages, setup

setup(
    name='ziemagent',
    version='3.34',
    packages=['ziemagent'],
    #install_requires=['ziem>=2.0'],
    entry_points={
    'console_scripts': [
        'ziemagent = ziemagent.__main__:main',
        ]
    },
)
