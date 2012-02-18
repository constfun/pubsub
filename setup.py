from setuptools import setup, find_packages
import os

setup(name='pubsub',
      version='0.1.0',
      packages=find_packages(),
      author='Nick Zalutskiy',
      author_email='pacemkr@{nospam}gmail.com',
      url='https://github.com/pacemkr/pubsub',
      include_package_data=True,
      description="Thread safe PubSub component with Qt Signals like API. Built using ØMQ (zeromq) sockets.",
      platforms=['any'],
)
