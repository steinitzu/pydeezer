from setuptools import setup, find_packages

requires = [
    'requests'
]

setup(
    name='pydeezer',
    version='1.0.0',
    description='A simple Python wrapper for Deezer\'s API',
    url='https://github.com/rcrdclub/pydeezer',
    author='Hery Ratsimihah',
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ),
    keywords='deezer api library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requires
)