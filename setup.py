from setuptools import setup

setup(
    name='h2p_parser',
    version='1.0.0',
    packages=[''],
    package_dir={'': 'h2p_parser'},
    install_requires=['nltk', 'inflect'],
    python_requires='>=3.7',
    url='https://github.com/ionite34/h2p-parser',
    license='Apache 2.0',
    author='ionite',
    author_email='dev@ionite.io',
    description='Heteronym to Phoneme Parser'
)
