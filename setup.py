from setuptools import setup, find_packages

from opencanary_correlator import __version__

setup(
    name='opencanary-correlator',
    version=__version__,
    url='http://www.thinkst.com/',
    author='Thinkst Applied Research',
    author_email='info@thinkst.com',
    description='opencanary correlator',
    install_requires=[
        "simplejson",
        "cffi",
        "docopt",
        "httplib2",
        "mandrill",
        "pycparser",
        "PyNaCl",
        "pytz",
        "redis",
        "requests",
        "six",
        "twilio",
        "Twisted",
        "wheel",
        "zope.interface"
    ],
    setup_requires=[
        'setuptools_git'
    ],
    license='BSD',
    packages = find_packages(exclude="test"),
    scripts=['bin/opencanary-correlator'],
    platforms='any',
    include_package_data=True,
)
