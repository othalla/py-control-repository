import setuptools

version = "0.2.0"


setuptools.setup(
    name="py-control-repository",
    version=version,
    description="Molule to manage Puppet control repository hosted on Github",
    author="Florian Chardin",
    author_email="othalla.lf@gmail.com",
    url="",
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
        "Topic :: Software Development",
    ],
    install_requires=[
        "PyGithub>=1.43",
    ],
    extras_require={},
    scripts=['scripts/type_checker.sh'],
)
