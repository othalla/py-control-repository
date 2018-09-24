import setuptools
import textwrap

version = "0.1.1"


setuptools.setup(
    name="py-control_repository",
    version=version,
    description="Module to manage puppet control repository hosted on Github",
    author="Florian Chardin",
    author_email="othalla.lf@gmail.com",
    url="",
    long_description=textwrap.dedent("""\
            To be done"""),
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
    extras_require={}
)
