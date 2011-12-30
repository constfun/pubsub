from setuptools import setup, find_packages
import os

DESCRIPTION = "Thread safe PubSub component with Qt Signals like API. Built using ØMQ (zeromq) sockets."

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass


setup(name='pubsub',
      version='0.1.0',
      packages=find_packages(),
      author='Nick Zalutskiy',
      author_email='pacemkr@{nospam}gmail.com',
      url='https://github.com/pacemkr/pubsub',
      include_package_data=True,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
)
