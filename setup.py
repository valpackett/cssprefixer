#!/usr/bin/env python
#import sys
from distutils.core import setup

# if sys.version < '2.5':
#     sys.exit('Python 2.5 or higher is required')

setup(name='cssprefixer',
      version='1.2.1',
      description="A tool that rewrites your CSS files, adding vendor-prefixed versions of CSS3 rules.",
#      long_description="""""",
      license='Apache License 2.0',
      author='myfreeweb',
      author_email='me@myfreeweb.ru',
      url='http://github.com/myfreeweb/cssprefixer',
      packages=['cssprefixer'],
      scripts=['scripts/cssprefixer'],
      keywords=['CSS', 'Cascading Style Sheets'],
      classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
      ],
      package_data={},
)
