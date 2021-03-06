from setuptools import setup, find_packages


setup(
    name='destral',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/gisce/destral',
    install_requires=[
        'osconf',
        'expects',
        'click'
    ],
    license='GNU GPLv3',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    entry_points={
        'console_scripts': [
            'destral = destral.cli:destral'
        ]
    },
    description=''
)
