from setuptools import setup
from pycdek3 import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pycdek',
    url='http://github.com/AlekseevAV/pycdek/',
    version=__version__,
    description='Python3 client for CDEK API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alekseev Aleksandr',
    author_email='alekseevavx@gmail.com',
    license='MIT',
    packages=['pycdek3'],
    package_data={'pycdek3': [
        'pycdek3/*.py',
    ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.4',
)
