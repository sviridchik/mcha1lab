from setuptools import setup

setup(name='Isp2lr',
      version='1.0',
      description='Python Distribution Utilities',
      author='VictoriaSv',
      author_email='viccisviri@gmail.com',
      packages=['serializations', 'services'],
      # install_requires=['PyYAML', 'toml'],
      scripts=['bin/magic.py'],
      test_suit='tests')
