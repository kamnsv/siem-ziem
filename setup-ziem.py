from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

packeges = find_packages()
packeges.remove('ziemagent')

print(packeges)

setup(
    name='ziem',
    version='3.55',
    packages=packeges,
    include_package_data = True,
    install_requires=required,
    entry_points={
    'console_scripts': [
        'ziem = ziem.__main__:main',
        ]
    },
    python_requires=">=3.9"
)