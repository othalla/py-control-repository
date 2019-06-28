import setuptools

version = "1.0.0"


setuptools.setup(
    name="py-control-repository",
    version=version,
    description="Module to manage Puppet control repository hosted on Github",
    author="Florian Chardin",
    author_email="othalla.lf@gmail.com",
    url="https://github.com/othalla/py-control-repository",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(exclude=['tests*']),
    package_data={},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
    install_requires=[
        "PyGithub>=1.43",
        "cliff==2.15.0",
    ],
    extras_require={},
    entry_points={
        'console_scripts': ['control_repository=control_repository.bin.__init__:main']
    }
)
