from setuptools import setup, find_packages

with open("requirements.txt") as requirements:
    install_requires = requirements.readlines()

with open("dev-requirements.txt") as dev_requirements:
    dev_requires = dev_requirements.readlines()

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="Chroot Tasker",
    version="0.1",
    author="Adam Dangoor",
    description="Create tasks in chroot jails.",
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
    classifiers=[
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points='''
        [console_scripts]
        tasker=cli.cli:cli
    ''',
)
