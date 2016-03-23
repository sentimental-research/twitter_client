from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]


setup(name='TwitterClient',
      version='0.1',
      description='The best twitter client in the world for research software',
      url='https://github.com/sentimental-research/twitter_client',
      author='Raquel Alegre and Olivier',
      author_email='raquel.alegre@world.gov',
      license='MIT',
      packages=['TwitterClient'],
      install_requires=reqs,
      zip_safe=False)
