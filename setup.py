from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name             = 'dnsimple',
    author           = 'Patrick Reagan',
    author_email     = 'reaganpr@gmail.com',
    url              = 'https://github.com/vigetlabs/dnsimple',
    version          = '0.1.0',
    description      = 'Library to manage domains and DNS records with DNSimple',
    long_description = readme,
    packages         = find_packages(include = ('dnsimple',)),
    install_requires = ['requests>=2.10.0,<2.11.0'],
    license           = 'MIT'
)
