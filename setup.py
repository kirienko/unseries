from setuptools import setup

with open('README.rst') as fd:
    readme = fd.read()

setup(
    name='unseries',
    version='0.0.4',
    packages=[''],
    platforms=['Linux', 'Unix', 'MacOsX', 'Windows'],
    url='https://github.com/kirienko/unseries',
    license='GPL-3.0',
    author='Yury Kirienko',
    author_email='yury.kirienko@gmail.com',
    description='Allows to deal with power series which coefficients contain uncertainties',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
    install_requires=['sympy', 'uncertainties>=3.0.1'],
)
