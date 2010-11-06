import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    README = CHANGES = ''

install_requires=['Pyparsing']
test_requires = ['zope.testing']

__version__ = "0.1"

setup(name='php_syntax',
      version=__version__,
      description='A php syntax parser that capable to read meadiawiki language files ',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: BSD-Like",
      ],
      url="http://github.com/avnik/php_syntax/",
      author="Alexander V. Nikolaev",
      author_email="avn@daemon.hole.ru",
      license="BSD-derived",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
      tests_require= test_requires,
      extras_require = {
          'test': test_requires,
      },
)

