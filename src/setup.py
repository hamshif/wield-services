from setuptools import setup, find_packages

setup(name='wield_services',
      version='0.1',
      description='A reactive debuggable CICD & orchestration management project'
                  'running a kubernetes micro-service cluster',
      url='https://github.com/hamshif/wild-services.git',
      author='gbar',
      author_email='hamshif@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['kubernetes', 'jprops']
      )
